from django.contrib import admin
from .models import Rearing, Cage, Rabbit

# Inline des lapins (dans une cage)
class RabbitInline(admin.TabularInline):
    model = Rabbit
    extra = 0
    fields = ['type', 'age', 'hunger', 'infection', 'is_pregnant']
    readonly_fields = ['hunger', 'infection', 'is_pregnant']

    def get_queryset(self, request):
        """
        Récupère tous les lapins, mais en optimisant avec les cages pour remonter jusqu'à l'élevage.
        """
        qs = super().get_queryset(request)
        return qs.select_related('cage__rearing')

# Inline des cages, avec les lapins dans chaque cage
class CageInline(admin.TabularInline):
    model = Cage
    extra = 0
    show_change_link = True

# Admin principal pour les élevages
@admin.register(Rearing)
class RearingAdmin(admin.ModelAdmin):
    list_display = ('rearing_name', 'game', 'current_money', 'current_food', 'total_cages', 'total_rabbits')
    search_fields = ('rearing_name',)
    list_filter = ('game',)
    inlines = [CageInline]

    def total_rabbits(self, obj):
        """
        Retourne le nombre total de lapins dans l'élevage (toutes cages confondues).
        """
        return Rabbit.objects.filter(cage__rearing=obj).count()
    total_rabbits.short_description = 'Total de lapins'

    def total_cages(self, obj):
        """
        Retourne le nombre de cages de l’élevage.
        """
        return obj.cages.count()
    total_cages.short_description = 'Nombre de cages'

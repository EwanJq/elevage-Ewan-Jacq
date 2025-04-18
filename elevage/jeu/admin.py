from django.contrib import admin
from .models import Rearing, Cage, Rabbit


# Inline des cages, avec les lapins dans chaque cage
class CageInline(admin.TabularInline):
    model = Cage
    extra = 0
    show_change_link = True

# Inline des lapins (dans une cage)
class RabbitInline(admin.TabularInline):
    model = Rabbit
    extra = 0
    fields = ['type', 'age', 'hunger', 'infection', 'is_pregnant']
    # Retirer readonly_fields si tu veux pouvoir modifier ces champs
    # readonly_fields = ['hunger', 'infection', 'is_pregnant']

# Admin des cages avec inline des lapins
@admin.register(Cage)
class CageAdmin(admin.ModelAdmin):
    list_display = ('id', 'rearing', 'rabbit_count')
    list_filter = ('rearing',)
    inlines = [RabbitInline]

    def rabbit_count(self, obj):
        return obj.rabbits.count()
    rabbit_count.short_description = 'Nombre de lapins'

# Admin principal des élevages avec inline des cages (sans les lapins directement ici)
@admin.register(Rearing)
class RearingAdmin(admin.ModelAdmin):
    list_display = ('rearing_name', 'game', 'current_money', 'current_food', 'total_cages', 'total_rabbits')
    search_fields = ('rearing_name',)
    list_filter = ('game',)
    inlines = [CageInline]  # Les cages visibles ici, mais lapins modifiables depuis CageAdmin

    def total_rabbits(self, obj):
        return Rabbit.objects.filter(cage__rearing=obj).count()
    total_rabbits.short_description = 'Total de lapins'

    def total_cages(self, obj):
        return obj.cages.count()
    total_cages.short_description = 'Nombre de cages'


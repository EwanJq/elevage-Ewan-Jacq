from django.contrib import admin
from .models import Game, Rearing, Cage, Rabbit

#permet d'enregistrer les modèles et d'inetragire avec eux via la plateforme administration (demande d'id ?)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_turn')
    search_fields = ('id', 'current_turn')

@admin.register(Rearing)
class RearingAdmin(admin.ModelAdmin):
    list_display = ('id', 'money', 'global_food')
    search_fields = ('id',)

@admin.register(Cage)
class CageAdmin(admin.ModelAdmin):
    list_display = ('id', 'cost', 'rearing')
    list_filter = ('rearing',)

@admin.register(Rabbit)
class RabbitAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'age', 'food', 'price', 'cage')
    list_filter = ('type', 'cage')
    search_fields = ('type', 'cage')


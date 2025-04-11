from django.urls import path
from . import views

app_name = "jeu"
urlpatterns = [
    path('setup/', views.game_setup, name='game_setup'),
    path('dashboard/', views.game_dashboard, name='game_dashboard') #la derniere url est celle à utiliser pour le redirect !
]


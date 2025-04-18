from django.urls import path
from . import views

app_name = "jeu"
urlpatterns = [
    path('menu', views.main_menu, name='main_menu'),  # On a la structure ( 'nom_barre_de_recherche', 'nom_code)
    path('setup/', views.game_setup, name='game_setup'),
    path('rearing/<str:rearing_name>/', views.rearing_dashboard, name='rearing_dashboard'),
    path('rearings/', views.all_rearings, name='all_rearings'),
]

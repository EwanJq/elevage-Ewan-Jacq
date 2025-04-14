from django.urls import path
from . import views

app_name = "jeu"
urlpatterns = [
    path('setup/', views.game_setup, name='game_setup'),
    path('rearing/<str:rearing_name>/', views.rearing_dashboard, name='rearing_dashboard'),
    path('rearing/<str:rearing_name>/next_turn/', views.next_turn, name='next_turn'),
]

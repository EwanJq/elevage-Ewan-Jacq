from django.urls import path
from . import views

app_name = "jeu"
urlpatterns = [
    path('setup/', views.game_setup, name='game_setup'),
]


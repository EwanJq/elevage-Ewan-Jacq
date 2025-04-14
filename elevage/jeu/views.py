from django.shortcuts import render, redirect
from .forms import *
from .models import *

def game_setup(request):
    if request.method == 'GET':
        form = GameSetupForm()                  #envoie les infos de la base de donnée à l'utilisateur
    elif request.method == 'POST':              #recupere les infos données par l'utilisateur
        form = GameSetupForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde les données dans la base de données
            return redirect('jeu:game_dashboard') # Redirige vers la page du jeu une fois l'initialisation terminée
    else:
        form = GameSetupForm()

    return render(request, 'jeu/setup.html', {'form': form})

    
def game_dashboard(request):
    
    setup = GameSetup.objects.last() #On récupere le dernier elevage crééer (A CHANGER)
    if not setup:
        return redirect('jeu:game_setup')

    if request.method == 'GET':
        dashboard_form = GameDashboardForm()
    if request.method == 'POST':
        dashboard_form = GameDashboardForm(request.POST)
        if dashboard_form.is_valid():
            
            # On traitera le tour 
            
            return redirect('jeu:game_dashboard') # On renvoie sur le jeu
    else:
        dashboard_form = GameDashboardForm()

    # Préparer les données à envoyer dans le contexte
    context = {
        'form': dashboard_form,
        'resources': {
            'argent': setup.initial_money,
            'nourriture': setup.initial_food,
            'mâles': setup.initial_male_rabbits,
            'femelles': setup.initial_female_rabbits,
            'jeunes': setup.initial_young_rabbits,
            'bébés': setup.initial_baby_rabbits,
        }
    }

    # Renvoyer le template avec le contexte
    return render(request, 'jeu/dashboard.html', context)
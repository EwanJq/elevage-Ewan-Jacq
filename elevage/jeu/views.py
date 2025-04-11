from django.shortcuts import render, redirect
from .forms import *
from .models import *

def game_setup(request):
    if request.method == 'GET':
        form = GameSetupForm()
    elif request.method == 'POST': #recupere les infos données par l'utilisateur
        form = GameSetupForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde les données dans la base de données
            return redirect('jeu:game_dashboard') # Redirige vers la page du jeu une fois l'initialisation terminée
    else:
        form = GameSetupForm()

    return render(request, 'jeu/setup.html', {'form': form})

def game_dashboard(request):
    # Récupérer le premier objet GameSetup, ou un spécifique si nécessaire
    setup = GameSetup.objects.first()  # ou GameSetup.objects.get(id=1) si tu sais quel objet tu veux

    # Si aucun GameSetup n'est trouvé, rediriger vers la page de setup
    if not setup:
        return redirect('jeu:game_setup')

    # Créer une instance du formulaire de dashboard
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
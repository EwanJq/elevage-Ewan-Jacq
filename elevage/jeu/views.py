from django.shortcuts import render, redirect
from .forms import GameSetupForm
from .models import GameSetup

def game_setup(request):
    if request.method == "POST": #recupere les infos données par l'utilisateur
        form = GameSetupForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde les données dans la base de données
            return redirect('game_dashboard')  # Redirige vers la page du jeu une fois l'initialisation terminée
        #creer une page de jeu dediée (nouveau html)
    else:
        form = GameSetupForm()

    return render(request, 'jeu/setup.html', {'form': form})



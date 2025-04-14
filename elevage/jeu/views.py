from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages  # Ajoutez cette ligne
from jeu.services import game_logic

def game_setup(request):
    if request.method == 'GET':
        form = GameSetupForm()                  #envoie les infos de la base de donnée à l'utilisateur
    elif request.method == 'POST':              #recupere les infos données par l'utilisateur
        form = GameSetupForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde les données dans la base de données
            game = Game.objects.create(current_turn=1)
            
            # Création de l'élevage avec les données du formulaire
            rearing = Rearing.objects.create(
                rearing_name=form.cleaned_data['rearing_name'],
                game=game,
                money=form.cleaned_data['initial_money'],
                global_food=form.cleaned_data['initial_food'],
                current_money=form.cleaned_data['initial_money'],
                current_food=form.cleaned_data['initial_food']
            )
            
            return redirect('jeu:rearing_dashboard', rearing_name=rearing.rearing_name) # Redirige vers la page du jeu une fois l'initialisation terminée
    else:
        form = GameSetupForm()

    return render(request, 'jeu/setup.html', {'form': form})



def rearing_dashboard(request, rearing_name):
    rearing = get_object_or_404(Rearing, rearing_name=rearing_name)
    return render(request, 'jeu/dashboard.html', {'rearing': rearing})

def next_turn(request, rearing_name):
    rearing = get_object_or_404(Rearing, rearing_name=rearing_name)
    
    success = game_logic.process_turn(request, rearing_name)  
    
    if success:
        rearing = get_object_or_404(Rearing, rearing_name=rearing_name)
        return redirect('jeu:rearing_dashboard', rearing_name=rearing.rearing_name)
    else:
        # Gérer l'erreur si nécessaire
        return redirect('jeu:rearing_dashboard', rearing_name=rearing_name)
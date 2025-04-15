from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from jeu.services.game_logic import buy_item, process_turn


# 0 -- Vue de Setup : lors de la creation de son premier élevage

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

    return render(request, 'jeu/setup.html', {'form': form})

# 1 -- Création du next turn effect, permettant de passer un mois dans le jeu


def next_turn(request, rearing_name):
    rearing = get_object_or_404(Rearing, rearing_name=rearing_name)
    
    success = process_turn(request, rearing_name)                # On applique la methode du process turn pour appliquer les effets du mois à tous les objets
    
    if success:
        rearing = get_object_or_404(Rearing, rearing_name=rearing_name)
        return redirect('jeu:rearing_dashboard', rearing_name=rearing_name)
    else:
        # Gérer l'erreur si nécessaire
        return redirect('jeu:rearing_dashboard', rearing_name=rearing_name)


# 2 -- Dashboard du jeu : Menu principal en jeu


def rearing_dashboard(request, rearing_name):
    rearing = get_object_or_404(Rearing, rearing_name=rearing_name)
    
    if request.method == 'GET':
        form = BuyItemForm()  
    elif request.method == 'POST':
        form = BuyItemForm(request.POST)
        if form.is_valid():
            item_type = form.cleaned_data['item_type']
            quantity = form.cleaned_data['quantity']
            buy_item(rearing_name, item_type, quantity)
            return redirect('jeu:rearing_dashboard', rearing_name=rearing_name)

    return render(request, 'jeu/dashboard.html', {'form': form, 'rearing': rearing})



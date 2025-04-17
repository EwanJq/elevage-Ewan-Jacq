from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from jeu.services.game_logic import buy_item, process_turn, sell_item


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



def rearing_dashboard(request, rearing_name):
    rearing = get_object_or_404(Rearing, rearing_name=rearing_name)

    # Initialisation des formulaires
    buy_form = BuyItemForm()
    sell_form = SellItemForm()

    if request.method == 'GET':
        # Envoie les formulaires vides à l'utilisateur
        return render(request, 'jeu/dashboard.html', {
            'rearing': rearing,
            'buy_form': buy_form,
            'sell_form': sell_form,
        })

    elif request.method == 'POST':
        # Récupère le type de formulaire soumis
        form_type = request.POST.get('form_type')

        if form_type == 'buy':
            buy_form = BuyItemForm(request.POST)
            if buy_form.is_valid():
                item_type = buy_form.cleaned_data['item_type']
                quantity = buy_form.cleaned_data['quantity']
                buy_item(rearing_name, item_type, quantity)

        elif form_type == 'sell':
            sell_form = SellItemForm(request.POST)
            if sell_form.is_valid():
                item_type = sell_form.cleaned_data['item_type']
                quantity = sell_form.cleaned_data['quantity']
                sell_item(rearing_name, item_type, quantity)

        elif form_type == 'next_turn':
            process_turn(request, rearing_name)

        # Redirection après traitement POST pour éviter une double soumission
        return redirect('jeu:rearing_dashboard', rearing_name=rearing_name)


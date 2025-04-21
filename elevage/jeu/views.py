from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from jeu.services.game_logic import buy_item, process_turn, sell_item, initialisation


# 0 -- Vue de Setup : lors de la creation de son premier élevage


def game_setup(request):
    if request.method == 'GET':
        form = GameSetupForm()

    elif request.method == 'POST':
        form = GameSetupForm(request.POST)
        if form.is_valid():
            setup_data = form.save()

            # Création de la partie
            game = Game.objects.create(current_turn=1)

            # Création de l’élevage
            rearing = Rearing.objects.create(
                rearing_name=setup_data.rearing_name,
                game=game,
                current_money=setup_data.initial_money,
                current_food=setup_data.initial_food
            )

            # Appel à la fonction qui se charge du setup complet (cages, lapins, répartition)
            initialisation(rearing, setup_data)

            # Nettoyage
            setup_data.delete()

            return redirect('jeu:rearing_dashboard', rearing_name=rearing.rearing_name)

    return render(request, 'jeu/setup.html', {'form': form})


# 1 -- Vue principale du jeu

    
def rearing_dashboard(request, rearing_name):
    # Récuperation de l'elevage et de ses données 
    rearing = get_object_or_404(Rearing, rearing_name=rearing_name) 
    rabbits = Rabbit.objects.filter(cage__rearing=rearing)
    cages = Cage.objects.filter(rearing=rearing)
    
    # Calculer le nombre total de lapins et de cages
    total_rabbits = rabbits.count()
    total_cages = cages.count()
    #Affichage du fond d'ecran selon le mois
    month = (rearing.game.current_turn) % 12
    if month in [1, 2, 3]:
        background = 'printemps.png'
    elif month in [4, 5, 6]:
        background = 'ete.png'
    elif month in [7, 8, 9]:
        background = 'automne.png'
    else:
        background = 'hiver.png'

    # Initialisation des formulaires
    buy_form = BuyItemForm()
    sell_form = SellItemForm()

    if request.method == 'GET':
        # Envoie les formulaires vides à l'utilisateur
        return render(request, 'jeu/dashboard.html', {
            'rearing': rearing,
            'rabbits': rabbits,
            'total_rabbits': total_rabbits,
            'total_cages': total_cages,
            'buy_form': buy_form,
            'sell_form': sell_form,
            'background_image': f"jeu/images/{background}"
        })

    elif request.method == 'POST':
        # Récuperation du formulaire
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
    
    
# 2 -- Vue de tous les élevages
    
    
def all_rearings(request):
    # Récupère tous les élevages
    rearings = Rearing.objects.all()
    
    # Recherche d'élevage si un terme est passé dans les paramètres GET
    search_term = request.GET.get('search', '')
    if search_term:
        rearings = rearings.filter(rearing_name__icontains=search_term)

    return render(request, 'jeu/all_rearings.html', {
        'rearings': rearings,
        'search_term': search_term
    })
    
    
# 3 -- Menu du jeu


def main_menu(request):
    background_image = 'jeu/images/lapin2.png' if random.random() < 0.05 else 'jeu/images/lapin1.png'
    return render(request, 'jeu/main_menu.html', {'background_image': background_image})




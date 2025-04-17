from django.shortcuts import render, redirect
from django.contrib import messages
from jeu.models import Rearing, Rabbit, Cage
import random
from django.db import transaction
from django.db import models


def process_turn(request, rearing_name):
    
    
    # Récuperation de l'elevage, vieillissement et application des règles de vie et de mort dans l'elevage
    try:
        rearing = Rearing.objects.get(rearing_name=rearing_name)
    except Rearing.DoesNotExist:
        return False, "Élevage non trouvé"
    
    
    # 0 -- Gestion des ages des lapins
    
    
    rabbits = Rabbit.objects.filter(cage__rearing=rearing).select_related('cage')
    for rabbit in rabbits :
        rabbit.update_age()         #methode de la classe lapin permettant de les faire vieillir et changer de stade de vie
    # cage__rearing=rearing permet de filtrer sur toutes cages appartenant à rearing
    
    
    # 1 -- Gestion des naissances


    pregnant_rabbits = Rabbit.objects.filter(
        is_pregnant=True,
        pregnancy_start=rearing.game.current_turn - 1  # filtre sur les femmelles enceintes depuis 1 mois ( gestation de 1 mois)
    )
    for mother in pregnant_rabbits:
        babies = random.randint(1, 4)
        for _ in range(babies):  #on creer des nouveaux lapins selon  le nombre de bebés crees 
            Rabbit.objects.create(
                type='baby',
                age=0,
                cage=mother.cage
            )
        mother.is_pregnant = False
        mother.save()
        
    
    # 2 -- Gestion des nouveaux accouplements
    
    
    females = Rabbit.objects.filter(
        type='female',                                  # On cherche une femelle
        age__gte=6,                                     # On cherche un lapin d'age superieur ou egal à 6 mois
        is_pregnant=False,                              # On ne veut pas qu'elle soit enceinte
    )
    
    for female in females:
    
        male_in_same_cage = Rabbit.objects.filter( # On vérifie s'il y a au moins un mâle adulte dans la meme cage
        cage=female.cage,
        type='male',
        age__gte=6 
        ).exists()

        if male_in_same_cage and random.random() < 0.3:     # Besoin d'un facteur chance pour ne pas surpeupler les cages trop facilement
            female.is_pregnant = True
            female.pregnancy_start = rearing.game.current_turn
            female.save()
            
        
    # 3 -- Gestion de l'entretien alimentaire des lapins
    
    
    FOOD_CONSUMPTION = {  # consommation en kg/mois
    'baby': 0,    
    'young': 3,   
    'male': 7.5,    
    'female': 7.5   
    }
        
    rabbits = Rabbit.objects.filter(cage__rearing=rearing).select_related('cage')
    # Permet de prendre tous les lapins en compte
    
    for rabbit in rabbits:
        consumption = FOOD_CONSUMPTION[rabbit.type]
        if rearing.current_food >= 0 :
            rearing.current_food -= consumption
            rabbit.hunger = max(0, rabbit.hunger - 15)          # Cap à 0
            rabbit.save()
            rearing.save()
        else :
            rabbit.hunger = min(100, rabbit.hunger + 40)        # Cap à 100
            rabbit.save()
            rearing.save()
            
    
    # 4 -- Gestion de l'espace disponible des cages (infections + morts)
    
    
    for cage in rearing.cages.all():
        rabbit_count = cage.rabbit_set.count()
    
        if rabbit_count <= 6:
            for rabbit in cage.rabbit_set.all():
                rabbit.infection = max(0, rabbit.infection - 15)
                rabbit.save()

        if rabbit_count > 6:
            infected_rabbits = cage.rabbit_set.order_by('?')[:max(1, rabbit_count - 6)]
            for rabbit in infected_rabbits:
                rabbit.infection = min(100, rabbit.infection + 40)
                rabbit.save()
        

        excess = max(0, rabbit_count - 10)

        if excess > 0:
            survie = 0.5
            n_to_kill = max(1, round(excess * survie))
            victims = cage.rabbit_set.order_by('?')[:n_to_kill]
            victims.delete()
            print(f"{n_to_kill} lapins morts de surpopulation dans la cage {cage.id}")
        
    
    # 5 -- Gestion des lapins infectés ou affamés
    
    
    for rabbit in Rabbit.objects.filter(cage__rearing=rearing):

        if rabbit.hunger > 50:
            if random.random() < rabbit.hunger / 200:  # 25% max de chance de mourir
                rabbit.delete()
                continue
        
        # Lapins infectés (infection > 50%)
        if rabbit.infection > 50:
            if random.random() < rabbit.infection / 200:  # 25% max de chance de mourir
                rabbit.delete()
                continue
        
        # Sauvegarde si le lapin survit
        rabbit.save()

    
    # 6 -- Passage du mois
    
    
    rearing.game.current_turn += 1
    rearing.game.save()
    

# Fonctions d'interactions entre l'utilisateur et la base de donnée
    
    
# Prix et constantes
PRICES_BUY = {
        'food': 1.2,  
        'cage': 70,    
        'baby': 10,
        'young': 15,
        'male': 20,
        'female': 25
}
PRICES_SELL = {
        'cage': 30,    
        'male': 15,
        'female': 20
}

def buy_item(rearing_name, item_type, quantity):

    rearing = Rearing.objects.get(rearing_name=rearing_name)
    unit_price = PRICES_BUY[item_type]
    total_cost = unit_price * quantity

    if item_type == 'food':
        rearing.current_food += quantity
        rearing.current_money -= total_cost
        rearing.save()
        
    elif item_type == 'cage':
        while quantity > 0 :
            Cage.objects.create(rearing=rearing)
            quantity -= 1
        rearing.current_money -= total_cost
        rearing.save()
        
    elif item_type in ['baby', 'young', 'male', 'female']:
        
        counter = quantity
        
        available_cages = rearing.cages.annotate(
            rabbit_count=models.Count('rabbit')
        ).filter(rabbit_count__lt=10).order_by('rabbit_count') 
        
        if available_cages == 0 :
            raise ValueError("Vous devez acheter une cage avant d’acheter des lapins.")
        
        for cage in available_cages:
            if cage.rabbit_set.count() <= 10 and  counter > 0:

                Rabbit.objects.create(
                    type=item_type,
                    age={'baby': 0, 'young': 1, 'male': 3, 'female': 3}[item_type],
                    cage=cage,
                    hunger=0,
                    infection=0
                    )
                counter -= 1
            else :
                None

        while counter > 0 :
            Rabbit.objects.create(
                type=item_type,
                age={'baby': 0, 'young': 1, 'male': 3, 'female': 3}[item_type],
                cage=rearing.cages.first(),
                hunger=0,
                infection=0
                )
            counter -= 1
                
        rearing.current_money -= total_cost
        rearing.save()
                
# A l'instar de buy_items qui marche très bien
def sell_item(rearing_name, item_type, quantity):
    rearing = Rearing.objects.get(rearing_name=rearing_name)
    unit_price = PRICES_SELL[item_type]
    total_gain = unit_price * quantity 

    if item_type == 'food':
        if rearing.current_food < quantity:
            raise ValueError("Pas assez de nourriture à vendre.")
        rearing.current_food -= quantity
        rearing.current_money += total_gain
        rearing.save()

    elif item_type == 'cage':
        # On récupère uniquement les cages vides
        empty_cages = rearing.cages.annotate(
            rabbit_count=models.Count('rabbit')
        ).filter(rabbit_count=0)[:quantity]

        if empty_cages.count() < quantity:
            raise ValueError("Impossible de vendre une cage contenant des lapins.")

        for cage in empty_cages:
            cage.delete()

        rearing.current_money += total_gain
        rearing.save()

    elif item_type in ['male', 'female']:
        rabbits = list(Rabbit.objects.filter(cage__rearing=rearing, type=item_type).order_by('age')[:quantity])
        
        if len(rabbits) < quantity:
            raise ValueError(f"Pas assez de lapins de type {item_type} à vendre.")
        
        for rabbit in rabbits:
            rabbit.delete()
        
        rearing.current_money += total_gain
        rearing.save()
            

        
    


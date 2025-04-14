from django.shortcuts import render, redirect
from django.contrib import messages
from jeu import models
from jeu.models import Rearing, Rabbit, Cage
import random

def process_turn(request, rearing_name):
    # Récuperation de l'elevage, vieillissement et application des règles de vie et de mort dans l'elevage
    try:
        rearing = Rearing.objects.get(rearing_name=rearing_name)
    except Rearing.DoesNotExist:
        return False, "Élevage non trouvé"
    
    # 0 -- Gestion des ages des lapins
    
    
    rabbits = Rabbit.objects.filter(cage__rearing=rearing).select_related('cage')
    for rabbit in rabbits :
        rabbit.update_age()
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
            female.pregnancy_duration = 1                   # Gestation de 1 mois
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
        else :
            rabbit.hunger = min(100, rabbit.hunger + 40)        # Cap à 100
            rabbit.save()
    
    # 4 -- Gestion de l'espace disponible des cages (infections + morts)
    
    
    for cage in rearing.cages.all():
        rabbit_count = cage.rabbit_set.count()
        
        if rabbit_count <= 6:
            rabbit.infection = max(0, rabbit.infection - 15)  # Cap à 100
            rabbit.save()
    
        if rabbit_count > 6:
            infected_rabbits = cage.rabbit_set.order_by('?')[:max(1, rabbit_count - 6)]
            for rabbit in infected_rabbits:
                rabbit.infection = min(100, rabbit.infection + 40)  # Cap à 100
                rabbit.save()
            
        if rabbit_count > 10:
            excess = rabbit_count - 10
        
        survie = 0.5
        rabbits_to_kill = cage.rabbit_set.order_by('?')[:max(1, round(excess * survie))]     # On laisse à quelques lapins une chance de survie, mais en en tuant au moins 1
        victims = cage.rabbit_set.order_by('?')[:rabbits_to_kill]                            # ordre aleatoire avec ?
        victims.delete()
        
        # Option : Log pour le joueur
        print(f"{rabbits_to_kill} lapins morts de surpopulation dans la cage {cage.id}")
        
    
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
    

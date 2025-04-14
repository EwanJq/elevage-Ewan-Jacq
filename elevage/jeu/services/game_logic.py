from django.shortcuts import render, redirect
from django.contrib import messages
from jeu import models
from jeu.models import Rearing, Rabbit, Cage
import random

def next_turn(request):
    # Récuperation de l'elevage, vieillissement et application des règles de vie et de mort dans l'elevage
    rearing = Rearing.objects.first()  
    
    
    # 0 -- Gestion des ages des lapins
    
    
    Rabbit.objects.filter(cage__rearing=rearing).update(age=models.F('age') + 1)
    # cage__rearing=rearing permet de filtrer sur toutes cages appartenant à rearing
    # models.F('age') permet d'acceder au champ age de la base de donnée
    
    
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
        
    
    # 3 -- Passage du mois
    
    
    rearing.game.current_turn += 1
    rearing.game.save()
    
    messages.success(request, f"Mois {rearing.game.current_turn} terminé !")
    return redirect('dashboard')
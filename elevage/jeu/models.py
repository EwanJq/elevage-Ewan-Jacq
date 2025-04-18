import random
from django.db import models

class Game(models.Model):
    current_turn = models.IntegerField(default=1)

class Rearing(models.Model):
    
    rearing_name = models.CharField(max_length=20, unique=True)     # Attribut unique pour recuperer les elevages selon leur nom
    game = models.ForeignKey(Game, on_delete=models.CASCADE)        # Sers à compter le nombre de tour ( Rajouter des attributs de jeu si multijoueur)   
    current_money = models.FloatField(default=0)
    current_food = models.FloatField(default=0)

class Cage(models.Model):
    cost = models.FloatField(default=100.0)                         # cout par défaut de la cage
    rearing = models.ForeignKey(Rearing, on_delete=models.CASCADE, related_name='cages')    
        
class Rabbit(models.Model):
    
    RABBIT_TYPE_CHOICES = [     # On est obligé d'utiliser des tuples : pour ce qui est utilisé en base de donnée et ce qui est affiché à l'utilisateur
        ('baby', 'Lapereau'),
        ('young', 'Jeune'),
        ('male', 'Mâle'),
        ('female', 'Femelle'),
    ]
        
    type = models.CharField(
        max_length=10,
        choices=RABBIT_TYPE_CHOICES,
        default='baby',
    )
    
    age = models.IntegerField(default=0)                            # en mois
    cage = models.ForeignKey('Cage', on_delete=models.CASCADE)
    hunger = models.IntegerField(default=0)                         # 0-100 scale
    infection = models.IntegerField(default=0)                      # 0-100 scale
    is_pregnant = models.BooleanField(default=False)
    pregnancy_start = models.IntegerField(null=True, blank=True)    # mois de début de gestation
    
    #Methode de changement de classe selon l'age
    def update_age(self):
        self.age += 1
        # Mise à jour du type si nécessaire
        if self.age >= 2 and self.type in ['baby','young']: 
            self.type = 'female' if random.random() > 0.5 else 'male'
        if self.age == 1 and self.type in ['baby']: 
            self.type = 'young'
        self.save()

    
    
# Classes communiquant avec le joueur
# on stockera dans cette classe les informations données par l'utilisateur JUSTE pour l'initaialisation

class GameSetup(models.Model):
    rearing_name = models.CharField(max_length=100)
    initial_male_rabbits = models.IntegerField(default=0)
    initial_female_rabbits = models.IntegerField(default=0)
    initial_young_rabbits = models.IntegerField(default=0)
    initial_baby_rabbits = models.IntegerField(default=0)
    initial_food = models.FloatField(default=0)
    initial_money = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    
    

    


    
    



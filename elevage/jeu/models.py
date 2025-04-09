from django.db import models

class Game(models.Model):
    current_turn = models.IntegerField(default=1)

class Rearing(models.Model):
    name = models.CharField()
    money = models.FloatField()
    global_food = models.FloatField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Cage(models.Model):
    cost = models.FloatField()
    rearing = models.ForeignKey(Rearing, on_delete=models.CASCADE)
    
    def rabbit_count(self):
        return self.rabbit_set.count()

    def is_overcrowded(self):
        return self.rabbit_count() > 10

    def is_full(self):
        return self.rabbit_count() >= 6

class Rabbit(models.Model):
    
    RABBIT_TYPE_CHOICES = [ #on est obligé d'utiliser des tuples : pour ce qui est utilisé en base de donnée et ce qui est affiché à l'utilisateur
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
    
    age = models.IntegerField(default=0)
    food = models.FloatField(default=0)
    price = models.FloatField(default=0)
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE)
    
# on stockera dans cette classe les informations données par l'utilisateur

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
    
    

    


    
    



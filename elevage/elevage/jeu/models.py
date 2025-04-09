from django.db import models

class Game(models.Model):
    current_turn = models.IntegerField(default=1)

class Rearing(models.Model):
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
    
    class RabbitType(models.TextChoices):
        BABY = 'baby'
        YOUNG = 'young'
        MALE = 'male'
        FEMALE = 'female'
        
    type = models.CharField(
        max_length=10,
        choices=RabbitType.choices,
        default=RabbitType.BABY,
    )
    
    age = models.IntegerField(default=0)
    food = models.FloatField(default=0)
    price = models.FloatField(default=0)
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE)
    
    

    


    
    



from django import forms
from .models import *

class GameSetupForm(forms.ModelForm):
    class Meta:
        model = GameSetup
        fields = [
            'rearing_name', 
            'initial_young_rabbits', 
            'initial_baby_rabbits', 
            'initial_male_rabbits', 
            'initial_female_rabbits', 
            'initial_food', 
            'initial_money'
        ]
        
        labels = { #On change les noms anglais pour donner une interface plus comprehensible à l'utilisateur
        'rearing_name': "Nom de l'élevage",
        'initial_young_rabbits': "Nombre de jeunes lapins",
        'initial_baby_rabbits': "Nombre de bébés lapins",
        'initial_male_rabbits': "Nombre de mâles",
        'initial_female_rabbits': "Nombre de femelles",
        'initial_food': "Quantité de nourriture (g)",
        'initial_money': "Argent initial (€)",
    }

        widgets = {
            'rearing_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'élevage"}),
            'initial_young_rabbits': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_baby_rabbits': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_male_rabbits': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_female_rabbits': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_food': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_money': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    # Permet d'empecher l'envoi du form s'il n'est pas valide
        
    def clean_initial_young_rabbits(self):
        initial_young_rabbits = self.cleaned_data.get('initial_young_rabbits')
        if initial_young_rabbits < 0:
            raise forms.ValidationError("Le nombre de jeunes lapins ne peut pas être négatif.")
        return initial_young_rabbits
        
    def clean_initial_baby_rabbits(self):
        initial_baby_rabbits = self.cleaned_data.get('initial_baby_rabbits')
        if initial_baby_rabbits < 0:
            raise forms.ValidationError("Le nombre de bébés lapins ne peut pas être négatif.")
        return initial_baby_rabbits
    
    def clean_initial_male_rabbits(self):
        initial_male_rabbits = self.cleaned_data.get('initial_male_rabbits')
        if initial_male_rabbits < 0:
            raise forms.ValidationError("Le nombre de lapins mâles ne peut pas être négatif.")
        return initial_male_rabbits

    def clean_initial_female_rabbits(self):
        initial_female_rabbits = self.cleaned_data.get('initial_female_rabbits')
        if initial_female_rabbits < 0:
            raise forms.ValidationError("Le nombre de lapins femelles ne peut pas être négatif.")
        return initial_female_rabbits

    def clean_initial_food(self):
        initial_food = self.cleaned_data.get('initial_food')
        if initial_food < 0:
            raise forms.ValidationError("La quantité de nourriture ne peut pas être négative.")
        return initial_food

    def clean_initial_money(self):
        initial_money = self.cleaned_data.get('initial_money')
        if initial_money < 0:
            raise forms.ValidationError("L'argent initial ne peut pas être négatif.")
        return initial_money
    

class RearingSearchForm(forms.Form):
    rearing_name = forms.CharField(
        label="Nom de votre élevage",
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Entrez le nom exact de votre élevage'
        })
    )

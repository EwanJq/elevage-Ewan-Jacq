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
    

class GameDashboardForm(forms.ModelForm):
    class Meta:
        model = GameDashboard
        fields = [
            'food_purchased',
            'cages_purchased',
            'rabbits_sold_male',
            'rabbits_sold_female',
            'rabbits_sold_young',
            'rabbits_sold_baby',
        ]
        
        labels = { #On change les noms anglais pour donner une interface plus comprehensible à l'utilisateur
        'food_purchased' : "Achat en nourriture",
        'cages_purchased' : "Achat de cages",
        'rabbits_sold_male' : "Vente de lapins males",
        'rabbits_sold_female' : "Vente de lapins femelle",
        'rabbits_sold_young' : "Vente de jeunes lapins",
        'rabbits_sold_baby' : "Vente de bébés lapins",
    }

        widgets = {
            'food_purchased': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantité de nourriture à acheter (kg)',
                'min': 0
            }),
            'cages_purchased': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de cages à acheter',
                'min': 0
            }),
            'rabbits_sold_male': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lapins mâles à vendre',
                'min': 0
            }),
            'rabbits_sold_female': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lapins femelles à vendre',
                'min': 0
            }),
            'rabbits_sold_young': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lapereaux à vendre',
                'min': 0
            }),
            'rabbits_sold_baby': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bébés lapins à vendre',
                'min': 0
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Tu peux ajouter ici des validations croisées si besoin
        return cleaned_data

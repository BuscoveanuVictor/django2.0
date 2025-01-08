from django import forms
from .models import Instrument, Category
from django import forms
from .models import Category
import datetime
import re

class InstrumentFilterForm(forms.Form):
    model = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Caută după model...'
    }))
    
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Min'
    }))
    
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Max'
    }))
    
    category = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    type = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    min_rating = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Implicit'),
            ('price_low', 'Preț crescător'),
            ('price_high', 'Preț descrescător'),
            ('rating', 'După rating'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populăm dinamic opțiunile pentru categorie și tip
        categories = Category.objects.values_list('instrument', flat=True).distinct()
        self.fields['category'].choices = [('', 'Toate categoriile')] + [(c, c) for c in categories]
        
        types = Category.objects.values_list('type', 'type').distinct()
        self.fields['type'].choices = [('', 'Toate tipurile')] + list(types)


# Formularul de contact
class ContactForm(forms.Form):
    nume = forms.CharField(max_length=100, label='Nume')
    prenume = forms.CharField(max_length=100, label='Prenume')
    data_nasterii = forms.DateField(label='Data nasterii', error_messages={
            'invalid': 'Date trebuie sa fie in formatul an.luna.zi'
        }
    )
    email = forms.EmailField(label='Email', error_messages={
            'invalid': 'Introduceți o adresă de email validă.'
        }
    )
    confirm_email = forms.EmailField(label='Confirmare Email',required=True)
    tip_mesaj = forms.ChoiceField(label='Tip mesaj', 
    choices=[('1', 'Reclamatie'), ('2', 'Intrebare'), ('3', 'Review'),
             ('4', 'Cerere' ),('5', 'Programare')])
    subject = forms.CharField(max_length=100, label='Subiect', required=True)
    minim_zile_asteptare = forms.IntegerField(label='Minim zile asteptare')
    mesaj = forms.CharField(widget=forms.Textarea, label='Mesaj', required=True)


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Adresele de email nu coincid.")

        # VALIDARE VARSTA
        data_nastere = cleaned_data.get("data_nasterii")
        if data_nastere: 
            varsta = (datetime.date.today() - data_nastere).days // 365
            if varsta < 18:
                raise forms.ValidationError("Trebuie sa ai minim 18 ani.")
        else:
            raise forms.ValidationError("Data nașterii este obligatorie.")

        # VALIDARE MESAJ
        mesaj = cleaned_data.get("mesaj")
        re.sub(r'\W+', ' ', mesaj)
        lista_cuvinte =  mesaj.split();
        if len(lista_cuvinte) < 5:
            raise forms.ValidationError("Trebuie sa ai minim 5 cuvinte.")
        elif len(lista_cuvinte) > 100:
            raise forms.ValidationError("Trebuie sa ai maxim 100 de cuvinte.")
        
        for cuvant in lista_cuvinte:
            if not cuvant.isalnum():
                raise forms.ValidationError("Cuvintele trebuie sa fie alfanumerice.")
            if cuvant.find("http") != -1:
                raise forms.ValidationError("Cuvintele nu trebuie sa contin linkuri.")
            if cuvant[-1] != cleaned_data.get("nume"):
                raise forms.ValidationError("Mesajul trebuie sa se termine cu semnatura dumneavoastra.")
            
        print(lista_cuvinte)
        
        return cleaned_data
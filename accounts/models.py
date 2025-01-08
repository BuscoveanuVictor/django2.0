from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date
        

class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Numărul de telefon trebuie să fie în format: '+40123456789'"
            )
        ],
        unique=True
    )
    
    birth_date = models.DateField(
        null=True,
        help_text="Format: YYYY-MM-DD"
    )
    
    address = models.TextField(
        max_length=200,
        help_text="Adresa completă de livrare"
    )
    
    newsletter = models.BooleanField(
        default=False,
        help_text="Subscrie la newsletter"
    )
    
    cod = models.CharField(max_length=100,null=True, blank=True)
    email_confirmat = models.BooleanField(default=False, null=True, blank=True)
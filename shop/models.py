from django.db import models

# Create your models here.
class Instrument(models.Model):
    instrument_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    rating = models.FloatField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='instruments', null=True)

    class Meta:
        permissions = [
            ("perm_add_instrument", "Can add instrument"),
        ]
    def __str__(self):
        return f"{self.model}"

class Category(models.Model):

    INSTRUMENT_TYPES = [
        ('ELECTRIC', 'Electric'),
        ('ACOUSTIC', 'Acoustic'),
        ('ELECTRO-ACOUSTIC', 'Electro-Acoustic'),
    ]
    category_id = models.AutoField(primary_key=True)
    instrument = models.CharField(max_length=50, null=False) # poate fi chitara, bas, tobe, etc.
    type = models.CharField(
        max_length=20, 
        choices=INSTRUMENT_TYPES,
        default='ACOUSTIC'
    )
    def __str__(self):
        return f"{self.instrument} - {self.get_type_display()}"

class InstrumentImage(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='instruments/')
    primary_image = models.BooleanField(default=False)  # pentru a marca imaginea principală
    order = models.IntegerField(default=0)  # pentru a ordona imaginile
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.instrument.model} - {self.order}"

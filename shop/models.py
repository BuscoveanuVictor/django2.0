from django.db import models
from django.utils import timezone

# Create your models here.
class Instrument(models.Model):
    instrument_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    rating = models.FloatField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='instruments', null=True)
    stock = models.PositiveIntegerField(default=0)
    
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
    path = models.ImageField(upload_to='instruments/')
    primary_image = models.BooleanField(default=False)  # pentru a marca imaginea principală
    order = models.IntegerField(default=0)  # pentru a ordona imaginile
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.instrument.model} - {self.order}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    instrument = models.ManyToManyField(Instrument,related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PROCESSING')

    def __str__(self):
        return f"Comanda de la furnizorul {self.supplier} pentru instrumentul {self.instrument} care are {self.quantity} bucati si este in starea de {self.status} "


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"S-au comandat {self.quantity} bucati din instrumentul {self.instrument} care apartine comenzii {self.order} "
    

class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='discounts')
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=False)

    def __str__(self):
        return f"Discount {self.discount_percentage}% pentru {self.instrument.model}"

# import uuid
# class Vizualizare(models.Model):
#     utilizator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     produs = models.ForeignKey('Instrument', on_delete=models.CASCADE)
#     data_vizualizare = models.DateTimeField(auto_now_add=True)
#     class Meta:
#        # trebuie ordonate ca sa stiu ce vizualizari sunt cele mai recente
#        ordering = ['-data_vizualizare'] 


# class Promotie(models.Model):
#     class Meta:
#        ordering = ['-data_creare']

#     nume = models.CharField(max_length=100)
#     data_creare = models.DateTimeField(auto_now_add=True)
#     data_expirare = models.DateTimeField()
#     discount = models.IntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)]
#     )
#     cod_promotional = models.CharField(max_length=16, unique=True,blank=True)
#     categorii = models.JSONField() 
   
#     def save(self, *args, **kwargs):
#        if not self.cod_promotional:
#            self.cod_promotional = str(uuid.uuid4())[:16]
#        super().save(*args, **kwargs)



# class CartItem(models.Model):
#     cart_item_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items')
#     instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='cart_items')
#     quantity = models.PositiveIntegerField(
#         default=1,
#         validators=[MinValueValidator(1)]
#     )
#     added_date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-added_date']
#         unique_together = ['user', 'instrument']  # Un utilizator poate avea un singur CartItem per instrument

#     def clean(self):
#         from django.core.exceptions import ValidationError
#         # Verifică dacă cantitatea cerută nu depășește stocul disponibil
#         if self.quantity > self.instrument.stock.quantity:
#             raise ValidationError(f'Cantitatea solicitată ({self.quantity}) depășește stocul disponibil ({self.instrument.stock.quantity})')

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.username} are {self.quantity} bucăți din {self.instrument.model} în coș"
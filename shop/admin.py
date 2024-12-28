from django.contrib import admin
from .models import Instrument, Category, InstrumentImage
# Register your models here.

admin.site.register(Instrument)
admin.site.register(Category)
admin.site.register(InstrumentImage)


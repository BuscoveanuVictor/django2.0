from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.



"""
    Dupa ce creezi un user/superuser in admin
    care se creeaza doar prin introducerea unui
    username, email si parola poti sa te duci
    in pagina de admin si dupa ce dai click
    pe userul pe care doresti sa il editezi
    poti sa completezi/editezi toate campurile
    adaugandu-le in fieldsets si multe altele
"""

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'address']
    
    fieldsets = UserAdmin.fieldsets[:-1] + (
       ('Informații adiționale', {
           'fields': ('phone_number', 'address','birth_date'),
       }),
    )
    add_fieldsets =  UserAdmin.fieldsets[:-1] + (
       ('Informații adiționale', {
           'fields': ('phone_number', 'address','birth_date'),
       }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
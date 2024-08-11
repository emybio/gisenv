from django.contrib import admin
from .models import Sahis

@admin.register(Sahis)
class SahisAdmin(admin.ModelAdmin):
    list_display = ('isim', 'tc_kimlik_no', 'telefon', 'user')
    search_fields = ('isim', 'tc_kimlik_no', 'telefon','user')
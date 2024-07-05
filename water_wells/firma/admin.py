from django.contrib import admin
from .models import Firma

@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = ('isim', 'meslek', 'diploma_oda_sicil_no')
    search_fields = ('isim', 'meslek', 'diploma_oda_sicil_no')
    filter_horizontal = ('sahislar',)

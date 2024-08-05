from django.contrib import admin
from .models import Firma

@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = ('isim', 'meslek', 'diploma_oda_sicil_no','user')
    search_fields = ('isim', 'meslek', 'diploma_oda_sicil_no','user')
    #filter_horizontal = ('sahislar',)

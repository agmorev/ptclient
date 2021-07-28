from django.contrib import admin
from .models import Warranty
from references.models import VehicleType
from django.utils.translation import ugettext_lazy as _


@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user.username', 'vehicle', 'code', 'weight', 'payments', 'price')
    list_filter = ('vehicle')
   
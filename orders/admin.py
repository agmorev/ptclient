from django.contrib import admin
from .models import Order
from django.utils.translation import ugettext_lazy as _


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'regime', 'vehicle', 'exporter_name', 'created')
    list_filter = ('regime', 'vehicle')
    fieldsets = (

        (None, {
            'classes': ('wide',),
            'fields': ['user', 'order_number', ('regime','vehicle')]
        }),
        (_('1. Відправник вантажу'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ('exporter_name', 'exporter_address', 'exporter_code')
        }),
        (_('2. Інформація про вантаж'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('cargo_name', 'cargo_code'), ('cargo_number', 'cargo_addnumber'), ('cargo_value', 'cargo_currency'), 'cargo_duties']
        }),
    )
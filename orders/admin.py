from django.contrib import admin
from .models import Order
from references.models import Company
from django.utils.translation import ugettext_lazy as _


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'regime', 'vehicle', 'exporter', 'order_created')
    list_filter = ('regime', 'vehicle')
    fieldsets = (

        (_('ЗАЯВКА'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('order_number', 'order_created'), ('regime','vehicle')]
        }),
        (_('1. Учасники зовнішньоекономічної операції'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['customer', ('exporter', 'importer'), ('carrier', 'forwarder')]
        }),
        (_('2. Інформація про вантаж'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('cargo_name', 'cargo_code'), ('cargo_number', 'cargo_addnumber'), ('cargo_value', 'cargo_currency'), 'cargo_duties']
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ("customer", 'exporter', 'importer', 'carrier', 'forwarder'):
            kwargs["queryset"] = Company.objects.filter(user=request.user)        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
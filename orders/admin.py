from django.contrib import admin
from .models import Order, Goods, UploadDocs
from references.models import Company, CustomsOffice, CustomsRegime
from django.utils.translation import ugettext_lazy as _


class GoodsInline(admin.TabularInline):
    model = Goods
    extra = 1


class UploadDocsInline(admin.TabularInline):
    model = UploadDocs
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [GoodsInline, UploadDocsInline]
    list_display = ('order_number', 'order_created', 'regime', 'principal', 'vehicle', 'expired_date',)
    list_display_links = ('order_number', 'order_created', 'principal', 'expired_date',)
    list_filter = ('vehicle', 'regime')
    date_hierarchy = 'order_created'
    fieldsets = (

        (_('ЗАЯВКА'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['order_number', 'order_created']
        }),
        (_('УЧАСНИКИ ПРОЦЕДУРИ'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['principal', 'customs']
        }),
        (_('ПРОЦЕДУРА ГАРАНТУВАННЯ'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['procedure', 'regime', 'vehicle', 'customs_departure', 'customs_destination', 'expired_date']
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ('customer', 'principal'):
            kwargs["queryset"] = Company.objects.filter(user=request.user)  
        if db_field.name == 'customs':
            kwargs["queryset"] = CustomsOffice.objects.filter(office_code__endswith='000')
        if db_field.name == 'regime':
            kwargs["queryset"] = CustomsRegime.objects.filter(status=True)      
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
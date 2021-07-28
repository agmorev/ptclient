from django.contrib import admin
from .models import (
    CustomsEntityType,
    CustomsRegime, 
    VehicleType, 
    CompanyStatus,
    Company,
    # Carrier, 
    # Consignee, 
    # Consignor, 
    # Forwarder, 
    Document, 
    Currency, 
    CustomsOffice,
    Agent
)
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import ugettext_lazy as _


@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name')
    list_filter = ['doc_type']
    ordering = ['code']
    search_fields = ('code', 'name')
    fieldsets = (
        (_('КЛАСИФІКАТОР документів'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['code', 'name', 'doc_type'],
        }),
    )


@admin.register(Currency)
class CurrencyAdmin(ImportExportModelAdmin):
    list_display = ('currency_code', 'currency_letter', 'currency_name')
    ordering = ['currency_code']
    search_fields = ('currency_code', 'currency_letter', 'currency_name')
    fieldsets = (
        (_('КЛАСИФІКАТОР іноземних валют'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['currency_code', 'currency_letter', 'currency_name'],
        }),
    )


@admin.register(CustomsOffice)
class CustomsOfficeAdmin(ImportExportModelAdmin):
    list_display = ('office_code', 'office_attr', 'office_name')
    ordering = ['office_code']
    search_fields = ('office_code', 'office_attr', 'office_name', 'office_locality')
    fieldsets = (
        (_('КЛАСИФІКАТОР митних підрозділів'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [
                ('office_code', 'office_attr'), 
                ('office_name'),
                ('office_region', 'office_locality'), 
                ('office_zip', 'office_address'),
            ],
        }),
    )


@admin.register(CustomsEntityType)
class CustomsEntityTypeAdmin(ImportExportModelAdmin):
    list_display = ('entity_type', 'code', 'feature', 'type_code')
    ordering = ['entity_type']
    search_fields = ('entity_type', 'code', 'feature', 'type_code')
    list_filter = ('entity_type',)
    fieldsets = (
        (_('КЛАСИФІКАТОР митних режимів'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('entity_type', 'code', 'feature', 'type_code')],
        }),
    )


@admin.register(CustomsRegime)
class CustomsRegimeAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name')
    ordering = ['code']
    search_fields = ('code', 'name')
    list_filter = ('short_name',)
    fieldsets = (
        (_('КЛАСИФІКАТОР митних режимів'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('code', 'short_name'), 'name'],
        }),
    )


@admin.register(VehicleType)
class VehicleTypeAdmin(ImportExportModelAdmin):
    list_display = ('vehicle_code', 'vehicle_name')
    ordering = ['vehicle_code']
    list_filter = ('vehicle_type',)
    search_fields = ['vehicle_code', 'vehicle_name']
    fieldsets = (
        (_('КЛАСИФІКАТОР видів транспорту'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('vehicle_type', 'vehicle_type_code'), ('vehicle_code', 'vehicle_name')],
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'email', 'phone', 'blacklist')
    ordering = ['name']
    search_fields = ('name', 'code', 'country')
    list_filter = ('status', 'blacklist')
    fieldsets = (
        (_('КОМПАНІЯ'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('name', 'country'), ('code', 'tax'), 'director'],
        }),
        (_('АДРЕСА'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['address'],
        }),
        (_('КОНТАКТИ'), {
            'classes': ('wide', 'extrapretty'),
            'fields': [('email', 'phone')],
        }),
        (_('СТАТУС'), {
            'classes': ('wide', 'extrapretty'),
            'fields': ['status', 'blacklist'],
        }),
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()


# @admin.register(Carrier)
# class CarrierAdmin(admin.ModelAdmin):
#     list_display = ('carrier_name', 'carrier_address', 'carrier_code', 'carrier_tax')
#     ordering = ['carrier_name']
#     search_fields = ('carrier_name', 'carrier_address', 'carrier_code', 'carrier_tax')
#     list_filter = ('carrier_country',)
#     fieldsets = (
#         (_('ПЕРЕВІЗНИК'), {
#             'classes': ('wide', 'extrapretty'),
#             'fields': ['carrier_country', ('carrier_name', 'carrier_address'), ('carrier_code', 'carrier_tax')],
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         if getattr(obj, 'user', None) is None:
#             obj.user = request.user
#         obj.save()


# @admin.register(Consignor)
# class ConsignorAdmin(admin.ModelAdmin):
#     list_display = ('consignor_name', 'consignor_address', 'consignor_code', 'consignor_tax')
#     ordering = ['consignor_name']
#     search_fields = ('consignor_name', 'consignor_address', 'consignor_code', 'consignor_tax')
#     list_filter = ('consignor_country',)
#     fieldsets = (
#         (_('ВІДПРАВНИК'), {
#             'classes': ('wide', 'extrapretty'),
#             'fields': ['consignor_country', ('consignor_name', 'consignor_address'), ('consignor_code', 'consignor_tax')],
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         if getattr(obj, 'user', None) is None:
#             obj.user = request.user
#         obj.save()


# @admin.register(Consignee)
# class ConsigneeAdmin(admin.ModelAdmin):
#     list_display = ('consignee_name', 'consignee_address', 'consignee_code', 'consignee_tax')
#     ordering = ['consignee_name']
#     search_fields = ('consignee_name', 'consignee_address', 'consignee_code', 'consignee_tax')
#     list_filter = ('consignee_name',)
#     fieldsets = (
#         (_('ОДЕРЖУВАЧ'), {
#             'classes': ('wide', 'extrapretty'),
#             'fields': ['consignee_country', ('consignee_name', 'consignee_address'), ('consignee_code', 'consignee_tax')],
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         if getattr(obj, 'user', None) is None:
#             obj.user = request.user
#         obj.save()


# @admin.register(Forwarder)
# class ForwarderAdmin(admin.ModelAdmin):
#     list_display = ('forwarder_name', 'forwarder_address', 'forwarder_code', 'forwarder_tax')
#     ordering = ['forwarder_name']
#     search_fields = ('forwarder_name', 'forwarder_address', 'forwarder_code', 'forwarder_tax')
#     list_filter = ('forwarder_country',)
#     fieldsets = (
#         (_('ЕКСПЕДИТОР'), {
#             'classes': ('wide', 'extrapretty'),
#             'fields': ['forwarder_country', ('forwarder_name', 'forwarder_address'), ('forwarder_code', 'forwarder_tax')],
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         if getattr(obj, 'user', None) is None:
#             obj.user = request.user
#         obj.save()

admin.site.register(Agent)
admin.site.register(CompanyStatus)
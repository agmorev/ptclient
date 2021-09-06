from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from users.models import User


class WarrantyType(models.Model):
    name = models.CharField(
        _('вид послуги'),
        max_length=255,
        null=True,
        blank=True)
    description = models.TextField(
        _('опис послуги'),
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('вид послуги')
        verbose_name_plural = _('види послуг')
    
    def __str__(self):
        return str(' '.join([self.name]))


class Currency(models.Model):
    currency_code = models.CharField(
        _('код'),
        max_length=3,
        null=True,
        blank=True)
    currency_letter = models.CharField(
        _('літерний код'),
        max_length=3,
        null=True,
        blank=True)
    currency_name = models.CharField(
        _('назва'),
        max_length=255,
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('валюта')
        verbose_name_plural = _('валюти')
    
    def __str__(self):
        return str(' '.join([self.currency_letter]))


class Document(models.Model):
    code = models.CharField(
        _('код'),
        max_length=4,
        null=True,
        blank=True)
    name = models.CharField(
        _('найменування'),
        max_length=255,
        null=True,
        blank=True)
    doc_type = models.CharField(
        _('тип'),
        max_length=255,
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('документ')
        verbose_name_plural = _('документи')
    
    def __str__(self):
        return str(' | '.join([str(self.code), self.name]))


class CustomsOffice(models.Model):
    office_code = models.CharField(
        _('код'),
        max_length=8,
        null=True,
        blank=True)
    office_attr = models.CharField(
        _('ознака'),
        max_length=3,
        null=True,
        blank=True)
    office_name = models.CharField(
        _('назва'),
        max_length=255,
        null=True,
        blank=True)
    office_region = models.CharField(
        _('область'),
        max_length=255,
        null=True,
        blank=True)
    office_locality = models.CharField(
        _('пункт'),
        max_length=255,
        null=True,
        blank=True)
    office_zip = models.CharField(
        _('індекс'),
        max_length=5,
        null=True,
        blank=True)
    office_address = models.CharField(
        _('назва вулиці'),
        max_length=255,
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('митний підрозділ')
        verbose_name_plural = _('митні підрозділи')
    
    def __str__(self):
        return str(' '.join([self.office_code, self.office_name]))[:100]


class CustomsEntityType(models.Model):
    entity_type = models.CharField(
        _('напрямок переміщення'),
        max_length=30,
        null=True,
        blank=True)
    code = models.CharField(
        _('код напрямку'),
        max_length=2,
        null=True,
        blank=True)
    feature = models.CharField(
        _('особливості декларування'),
        max_length=255,
        null=True,
        blank=True)
    type_code = models.CharField(
        _('код типу'),
        max_length=2,
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('тип декларації')
        verbose_name_plural = _('типи декларацій')
    
    def __str__(self):
        return str(' '.join([self.entity_type, self.type_code]))


class CustomsRegime(models.Model):
    code = models.CharField(
        _('код'),
        max_length=2,
        null=True,
        blank=True)
    name = models.CharField(
        _('назва'),
        max_length=255,
        null=True,
        blank=True)
    short_name = models.CharField(
        _('скорочена назва'),
        max_length=255,
        null=True,
        blank=True)
    status = models.BooleanField(
        null=True,
        blank=True,
        verbose_name = _('гарантування'))
    
    class Meta:
        verbose_name = _('митний режим')
        verbose_name_plural = _('митні режими')
    
    def __str__(self):
        return str('.'.join([self.short_name, str(self.code)]))


class WarrantyProcedure(models.Model):
    code = models.CharField(
        _('код'),
        max_length=5,
        null=True,
        blank=True)
    name = models.CharField(
        _('назва'),
        max_length=255,
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('процедура гарантування')
        verbose_name_plural = _('процедури гарантування')
    
    def __str__(self):
        return str(' '.join([str(self.code), self.name]))


class VehicleType(models.Model):
    vehicle_type = models.CharField(
        _('тип транспорту'),
        max_length=255,
        null=True,
        blank=True)
    vehicle_type_code = models.CharField(
        _('код типу'),
        max_length=1,
        null=True,
        blank=True)
    vehicle_code = models.CharField(
        _('код транспорту'),
        max_length=2,
        null=True,
        blank=True)
    vehicle_name = models.CharField(
        _('назва'),
        max_length=255,
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = _('вид транспорту')
        verbose_name_plural = _('види транспорту')
    
    def __str__(self):
        return self.vehicle_name


# class CompanyStatus(models.Model):
#     status = models.CharField(
#         _('статус'),
#         max_length=255,
#         null=True,
#         blank=True)

#     class Meta:
#         ordering = ['status']
#         verbose_name = _('статус компанії')
#         verbose_name_plural = _('статуси компаній')

#     def __str__(self):
#         return self.status

class Company(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='user_company')
    name = models.CharField(
        _('назва'),
        max_length=255,
        null=True,
        blank=True)
    code = models.CharField(
        _('ЄДРПОУ'),
        max_length=8,
        null=True,
        blank=True)
    tax = models.CharField(
        _('ІПН'),
        max_length=10,
        null=True,
        blank=True)   
    address = models.CharField(
        _('адреса'),
        max_length=255,
        null=True,
        blank=True) 
    country = CountryField(
        _('країна'),
        blank_label=_('Оберіть країну...'),
        blank=True)
    director = models.CharField(
        _('керівник'),
        max_length=255,
        null=True,
        blank=True)
    email = models.EmailField(
        _('email'),
        null=True,
        blank=True)
    phone = PhoneNumberField(
        _('телефон'),
        null=True,
        blank=True)
    status = models.BooleanField(
        null=True,
        blank=True,
        default=True,
        verbose_name = _('активна'))
    blacklist = models.BooleanField(
        _('чорний список'),  
        null=True,      
        blank=True)

    class Meta:
        verbose_name = _('компанія')
        verbose_name_plural = _('компанії')

    def __str__(self):
        return self.name


# class Carrier(models.Model):
#     user = models.ForeignKey(
#         User,
#         null=False,
#         blank=False,
#         on_delete=models.CASCADE,
#         related_name='user_carrier')
#     carrier_country = CountryField(
#         _('країна реєстрації'),
#         blank_label=_('Оберіть країну...'),
#         blank=True)
#     carrier_name = models.CharField(
#         _('назва компанії'),
#         max_length=255,
#         null=True,
#         blank=True)
#     carrier_address = models.CharField(
#         _('адреса'),
#         max_length=255,
#         null=True,
#         blank=True)
#     carrier_code = models.CharField(
#         _('ЄДРПОУ/ДРФО'),
#         max_length=8,
#         null=True,
#         blank=True)
#     carrier_tax = models.CharField(
#         _('ІПН'),
#         max_length=12,
#         null=True,
#         blank=True)   
    
#     class Meta:
#         verbose_name = _('перевізник')
#         verbose_name_plural = _('перевізники')
    
#     def __str__(self):
#         return str(self.carrier_name)


# class Consignor(models.Model):
#     user = models.ForeignKey(
#         User,
#         null=False,
#         blank=False,
#         on_delete=models.CASCADE,
#         related_name='user_consignor')
#     consignor_country = CountryField(
#         _('країна реєстрації'),
#         blank_label=_('Оберіть країну...'),
#         blank=True)
#     consignor_name = models.CharField(
#         _('назва компанії'),
#         max_length=255,
#         null=True,
#         blank=True)
#     consignor_address = models.CharField(
#         _('адреса'),
#         max_length=255,
#         null=True,
#         blank=True)
#     consignor_code = models.CharField(
#         _('ЄДРПОУ/ДРФО'),
#         max_length=8,
#         null=True,
#         blank=True)
#     consignor_tax = models.CharField(
#         _('ІПН'),
#         max_length=12,
#         null=True,
#         blank=True)   
    
#     class Meta:
#         verbose_name = _('відправник')
#         verbose_name_plural = _('відправники')
    
#     def __str__(self):
#         return str(self.consignor_name)


# class Consignee(models.Model):
#     user = models.ForeignKey(
#         User,
#         null=False,
#         blank=False,
#         on_delete=models.CASCADE,
#         related_name='user_consignee')
#     consignee_country = CountryField(
#         _('країна реєстрації'),
#         blank_label=_('Оберіть країну...'),
#         blank=True)
#     consignee_name = models.CharField(
#         _('назва компанії'),
#         max_length=255,
#         null=True,
#         blank=True)
#     consignee_address = models.CharField(
#         _('адреса'),
#         max_length=255,
#         null=True,
#         blank=True)
#     consignee_code = models.CharField(
#         _('ЄДРПОУ/ДРФО'),
#         max_length=8,
#         null=True,
#         blank=True)
#     consignee_tax = models.CharField(
#         _('ІПН'),
#         max_length=12,
#         null=True,
#         blank=True)   
    
#     class Meta:
#         verbose_name = _('одержувач')
#         verbose_name_plural = _('одержувачі')
    
#     def __str__(self):
#         return str(self.consignee_name)


# class Forwarder(models.Model):
#     user = models.ForeignKey(
#         User,
#         null=False,
#         blank=False,
#         on_delete=models.CASCADE,
#         related_name='user_forwarder')
#     forwarder_country = CountryField(
#         _('країна реєстрації'),
#         blank_label=_('Оберіть країну...'),
#         blank=True)
#     forwarder_name = models.CharField(
#         _('назва компанії'),
#         max_length=255,
#         null=True,
#         blank=True)
#     forwarder_address = models.CharField(
#         _('адреса'),
#         max_length=255,
#         null=True,
#         blank=True)
#     forwarder_code = models.CharField(
#         _('ЄДРПОУ/ДРФО'),
#         max_length=8,
#         null=True,
#         blank=True)
#     forwarder_tax = models.CharField(
#         _('ІПН'),
#         max_length=12,
#         null=True,
#         blank=True)   
    
#     class Meta:
#         verbose_name = _('експедитор')
#         verbose_name_plural = _('експедитори')
    
#     def __str__(self):
#         return str(self.forwarder_name)


class Agent(models.Model):
    name = models.CharField(
        _('назва'), 
        max_length=255, 
        blank=True,
        null=True
    )
    vehicle = models.ForeignKey(
        VehicleType,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name='vehicles',
        verbose_name=_('транспорт')
    )
    country = CountryField(
        _('суміжна країна'),
        blank_label=_('Оберіть країну...'),
        blank=True,
        null=True
    )
    latitude = models.FloatField(
        _('широта'),
        blank=True,
        null=True
    )
    longitude = models.FloatField(
        _('довгота'),
        blank=True,
        null=True,
    )
    notes = models.TextField(
        _('примітки'), 
        max_length=255, 
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('представник')
        verbose_name_plural = _('представники')

    def __str__(self):
        return self.name
    

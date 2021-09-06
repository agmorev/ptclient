from django.db import models
from django.utils import timezone
from users.models import User
from references.models import Company, CustomsOffice, CustomsRegime, VehicleType, WarrantyProcedure, WarrantyType
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum


class Order(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name='user')
    order_number = models.PositiveIntegerField(
        _('№'),
        null=True,
        blank=True)
    order_created = models.DateField(
        _('дата створення'),
        default=timezone.now,
        null=True,
        blank=True)
    order_updated = models.DateField(
        _('дата редагування'),
        auto_now_add=True)
    warranty_type = models.ForeignKey(
        WarrantyType,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='warranty_type',
        verbose_name=_('послуга'))
    customs = models.ForeignKey(
        CustomsOffice,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='customs',
        verbose_name=_('бенефіціар'))
    procedure = models.ForeignKey(
        WarrantyProcedure,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='procedure',
        verbose_name=_('процедура'))
    regime = models.ForeignKey(
        CustomsRegime,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='regime',
        verbose_name=_('митний режим'))
    vehicle = models.ForeignKey(
        VehicleType,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='vehicle',
        verbose_name=_('транспорт'))
    # customer = models.ForeignKey(
    #     Company,
    #     null=True,
    #     blank=True,
    #     on_delete=models.DO_NOTHING,
    #     related_name='company_customer',
    #     limit_choices_to={'status': '1'},
    #     verbose_name=_('клієнт'))
    # exporter = models.ForeignKey(
    #     Company,
    #     null=True,
    #     blank=True,
    #     on_delete=models.DO_NOTHING,
    #     related_name='company_exporter',
    #     verbose_name=_('експортер'))
    # importer = models.ForeignKey(
    #     Company,
    #     null=True,
    #     blank=True,
    #     on_delete=models.DO_NOTHING,
    #     related_name='company_importer',
    #     verbose_name=_('імпортер'))
    # carrier = models.ForeignKey(
    #     Company,
    #     null=True,
    #     blank=True,
    #     on_delete=models.DO_NOTHING,
    #     related_name='company_carrier',
    #     verbose_name=_('перевізник'))
    # forwarder = models.ForeignKey(
    #     Company,
    #     null=True,
    #     blank=True,
    #     on_delete=models.DO_NOTHING,
    #     related_name='company_forwarder',
    #     verbose_name=_('експедитор'))
    principal = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='company_principal',
        verbose_name=_('принципал'))
    # cargo_name = models.CharField(
    #     _('найменування вантажу'),
    #     max_length=255,
    #     null=True,
    #     blank=True)
    # cargo_code = models.CharField(
    #     _('код УКТЗЕД'),
    #     max_length=10,
    #     null=True,
    #     blank=True)
    # cargo_number = models.CharField(
    #     _('кількість вантажу, кг.'),
    #     max_length=255,
    #     null=True,
    #     blank=True)
    # cargo_addnumber = models.CharField(
    #     _('кількість вантажу, додаткові одиниці виміру'),
    #     max_length=255,
    #     null=True,
    #     blank=True)
    # cargo_value = models.CharField(
    #     _('фактурна вартість товару з урахуванням транспортних видатків'),
    #     max_length=255,
    #     null=True,
    #     blank=True)
    # cargo_currency = models.CharField(
    #     _('валюта'),
    #     max_length=255,
    #     null=True,
    #     blank=True)
    # cargo_duties = models.CharField(
    #     _('сума митних платежів, на які надається фінансова гарантія, грн.'),
    #     max_length=255,
    #     null=True,
    #     blank=True)
    customs_departure = models.ForeignKey(
        CustomsOffice,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='customs_departure',
        verbose_name=_('митниця відправлення'))
    customs_destination = models.ForeignKey(
        CustomsOffice,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='customs_destination',
        verbose_name=_('митниця призначення'))
    expired_date = models.DateField(
        _('строк дії гарантії'),
        default=timezone.now,
        null=False,
        blank=False)
    
    def get_goods(self):
        return self.goods.filter(order=self.pk)
    
    def goods_total_number(self):
        return self.goods.filter(order=self.pk).aggregate(Sum('number'))['number__sum']
    
    def goods_total_duties(self):
        return self.goods.filter(order=self.pk).aggregate(Sum('duties'))['duties__sum']
    
    def get_docs(self):
        return self.uploaddocs.filter(order=self.pk)
   
    class Meta:
        verbose_name = _('заявка')
        verbose_name_plural = _('заявки')

    def __str__(self):
        return str(self.id)


class Goods(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='goods')
    name = models.CharField(
        _('назва'),
        max_length=255,
        null=True,
        blank=True)
    code = models.CharField(
        _('код УКТЗЕД'),
        max_length=10,
        null=True,
        blank=True)
    number = models.PositiveIntegerField(
        _('вага, кг.'),
        null=True,
        blank=True)
    addnumber = models.PositiveIntegerField(
        _('кількість'),
        null=True,
        blank=True)
    duties = models.PositiveIntegerField(
        _('платежі, грн.'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товари')

    def __str__(self):
        return str('-'.join([self.name, self.code]))


class UploadDocs(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='uploaddocs',        
    )
    doc_file = models.FileField(
        _('завантажити файл'),
        upload_to='uploads/documents/%Y/%m/%d/',
        null=True,
        blank=True
    )
    doc_name = models.CharField(
        _('назва документа'),
        max_length=255,
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('товаросупровідний документ')
        verbose_name_plural = _('товаросупровідні документи')

    def __str__(self):
        return str(self.order.order_number)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import User
from references.models import Company, CustomsRegime, VehicleType
from datetime import datetime


class Order(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name='user')
    order_number = models.CharField(
        _('номер заявки'),
        max_length=255,
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
        verbose_name=_('вид транспорту'))
    customer = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='company_customer',
        limit_choices_to={'status': '1'},
        verbose_name=_('клієнт'))
    exporter = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='company_exporter',
        limit_choices_to={'status': '2'},
        verbose_name=_('експортер'))
    importer = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='company_importer',
        limit_choices_to={'status': '3'},
        verbose_name=_('імпортер'))
    carrier = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='company_carrier',
        limit_choices_to={'status': '4'},
        verbose_name=_('перевізник'))
    forwarder = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='company_forwarder',
        limit_choices_to={'status': '5'},
        verbose_name=_('експедитор'))
    cargo_name = models.CharField(
        _('найменування вантажу'),
        max_length=255,
        null=True,
        blank=True)
    cargo_code = models.CharField(
        _('код УКТЗЕД'),
        max_length=10,
        null=True,
        blank=True)
    cargo_number = models.CharField(
        _('кількість вантажу, кг.'),
        max_length=255,
        null=True,
        blank=True)
    cargo_addnumber = models.CharField(
        _('кількість вантажу, додаткові одиниці виміру'),
        max_length=255,
        null=True,
        blank=True)
    cargo_value = models.CharField(
        _('фактурна вартість товару з урахуванням транспортних видатків'),
        max_length=255,
        null=True,
        blank=True)
    cargo_currency = models.CharField(
        _('валюта'),
        max_length=255,
        null=True,
        blank=True)
    cargo_duties = models.CharField(
        _('сума митних платежів, на які надається фінансова гарантія, грн.'),
        max_length=255,
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('заявка')
        verbose_name_plural = _('заявки')

    def __str__(self):
        return str(self.id)
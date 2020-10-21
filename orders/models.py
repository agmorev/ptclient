from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User


class Order(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='user')
    order_number = models.CharField(
        _('номер заявки'),
        max_length=255,
        null=True,
        blank=True)
    created = models.DateTimeField(
        _('дата створення'),
        auto_now_add=True)
    updated = models.DateTimeField(
        _('дата створення'),
        auto_now=True)
    regime = models.CharField(
        _('митний режим'),
        max_length=255,
        null=True,
        blank=True)
    vehicle = models.CharField(
        _('вид транспорту'),
        max_length=8,
        null=True,
        blank=True)
    exporter_name = models.CharField(
        _('найменування юридичної особи/фізичної особи-підприємця'),
        max_length=255,
        null=True,
        blank=True)   
    exporter_address = models.CharField(
        _('юридична адреса'),
        max_length=255,
        null=True,
        blank=True) 
    exporter_code = models.CharField(
        _('ЄДРПОУ'),
        max_length=8,
        null=True,
        blank=True)
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
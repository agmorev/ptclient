from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
from references.models import VehicleType
from django.core.validators import RegexValidator
from datetime import datetime


class Warranty(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name='user')
    created = models.DateTimeField(
        _('дата розрахунку'),
        auto_now=True)
    vehicle = models.ForeignKey(
        VehicleType,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='vehicle',
        verbose_name=_('вид транспорту'))
    code = models.CharField(
        _('код УКТЗЕД'),
        max_length=10,
        null=True,
        blank=True)
    weight = models.CharField(
        _('кількість вантажу, кг.'),
        max_length=255,
        null=True,
        blank=True)
    payments = models.CharField(
        _('сума митних платежів'),
        max_length=255,
        null=True,
        blank=True)
    price = models.CharField(
        _('вартість гарантії'),
        max_length=255,
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('гарантія')
        verbose_name_plural = _('гарантії')

    def __str__(self):
        return str(self.created)
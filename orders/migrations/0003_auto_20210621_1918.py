# Generated by Django 3.1.2 on 2021-06-21 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0008_auto_20210621_1845'),
        ('orders', '0002_auto_20210621_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_regime',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_vehicle',
        ),
        migrations.AddField(
            model_name='order',
            name='regime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='regime', to='references.customsregime', verbose_name='митний режим'),
        ),
        migrations.AddField(
            model_name='order',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vehicle', to='references.vehicletype', verbose_name='вид транспорту'),
        ),
        migrations.AlterField(
            model_name='order',
            name='exporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='company_exporter', to='references.company', verbose_name='експортер'),
        ),
    ]

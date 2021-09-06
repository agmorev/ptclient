# Generated by Django 3.1.2 on 2021-08-22 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0014_auto_20210822_1630'),
        ('orders', '0013_auto_20210822_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='warranty_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='types', to='references.warrantytype', verbose_name='послуга'),
        ),
    ]
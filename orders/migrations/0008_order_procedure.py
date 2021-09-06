# Generated by Django 3.1.2 on 2021-08-20 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0012_auto_20210820_2017'),
        ('orders', '0007_auto_20210820_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='procedure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='procedure', to='references.warrantyprocedure', verbose_name='процедура гарантування'),
        ),
    ]

# Generated by Django 3.1.2 on 2021-08-27 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0018_auto_20210827_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='customsregime',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='гарантування'),
        ),
    ]

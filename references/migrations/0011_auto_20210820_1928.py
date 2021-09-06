# Generated by Django 3.1.2 on 2021-08-20 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0010_customsregime_short_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarrantyProcedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=2, null=True, verbose_name='код')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='назва')),
            ],
            options={
                'verbose_name': 'процедура гарантування',
                'verbose_name_plural': 'процедури гарантування',
            },
        ),
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.ManyToManyField(blank=True, to='references.CompanyStatus', verbose_name='статус'),
        ),
    ]

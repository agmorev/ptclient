# Generated by Django 3.1.2 on 2021-04-17 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_employee_employee_education'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_notes',
            field=models.TextField(blank=True, verbose_name='примітки'),
        ),
    ]
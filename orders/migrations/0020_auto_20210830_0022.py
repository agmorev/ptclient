# Generated by Django 3.1.2 on 2021-08-29 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_auto_20210828_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploaddocs',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='uploaddocs', to='orders.order'),
            preserve_default=False,
        ),
    ]
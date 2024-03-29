# Generated by Django 3.1.2 on 2021-08-20 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20210821_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='warranty_sum',
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='назва')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='код УКТЗЕД')),
                ('number', models.PositiveIntegerField(blank=True, null=True, verbose_name='вага, кг.')),
                ('addnumber', models.PositiveIntegerField(blank=True, null=True, verbose_name='кількість')),
                ('duties', models.PositiveIntegerField(blank=True, null=True, verbose_name='платежі, грн.')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='orders.order')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товари',
            },
        ),
    ]

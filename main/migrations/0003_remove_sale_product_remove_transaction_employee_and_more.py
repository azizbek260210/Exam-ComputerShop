# Generated by Django 5.0.6 on 2024-05-18 05:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_product_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='product',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='product',
        ),
        migrations.CreateModel(
            name='EnterProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('entered_at', models.DateField(auto_now_add=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
            options={
                'ordering': ['-entered_at'],
            },
        ),
        migrations.CreateModel(
            name='SellProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('sold_at', models.DateField(auto_now_add=True)),
                ('refunded', models.BooleanField(default=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
            options={
                'ordering': ['-sold_at'],
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refunded_at', models.DateTimeField(auto_now_add=True)),
                ('sell_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.sellproduct')),
            ],
            options={
                'ordering': ['-refunded_at'],
            },
        ),
        migrations.DeleteModel(
            name='Return',
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
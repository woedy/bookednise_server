# Generated by Django 5.1 on 2024-11-27 06:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(blank=True, max_length=200, null=True)),
                ('private_api_key', models.CharField(blank=True, max_length=1000, null=True)),
                ('public_api_key', models.CharField(blank=True, max_length=1000, null=True)),
                ('reservation_policy_value', models.IntegerField(default=0)),
                ('reservation_policy_description', models.TextField(blank=True, null=True)),
                ('cancellation_policy_value', models.IntegerField(default=0)),
                ('cancellation_policy_description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_payment_setup', to='shop.shop')),
            ],
        ),
    ]

# Generated by Django 5.1 on 2024-11-27 06:40

import django.core.validators
import django.db.models.deletion
import shop.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=5000, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=shop.models.upload_service_category_photo_path)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(blank=True, max_length=200, null=True)),
                ('photo', models.ImageField(blank=True, default=shop.models.get_default_package_image, null=True, upload_to=shop.models.upload_package_photo_path)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('duration', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('shop_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('business_type', models.CharField(blank=True, choices=[('Private', 'Private'), ('Public', 'Public')], max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('cvr', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('business_days', models.CharField(blank=True, max_length=255, null=True)),
                ('business_hours_open', models.CharField(blank=True, max_length=255, null=True)),
                ('business_hours_close', models.CharField(blank=True, max_length=255, null=True)),
                ('special_features', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=2, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=shop.models.upload_shop_logo_path)),
                ('verify_code', models.CharField(blank=True, max_length=10, null=True)),
                ('open', models.BooleanField(default=True)),
                ('shop_registered', models.BooleanField(default=False)),
                ('shop_setup', models.BooleanField(default=False)),
                ('service_setup', models.BooleanField(default=False)),
                ('payment_setup', models.BooleanField(default=False)),
                ('staff_setup', models.BooleanField(default=False)),
                ('registration_complete', models.BooleanField(default=False)),
                ('street_address1', models.CharField(blank=True, max_length=255, null=True)),
                ('street_address2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=255, null=True)),
                ('location_name', models.CharField(blank=True, max_length=200, null=True)),
                ('digital_address', models.CharField(blank=True, max_length=200, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=15, default=0.0, max_digits=30, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=15, default=0.0, max_digits=30, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShopExterior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=shop.models.upload_shop_exterior_path)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_exterior', to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShopInterior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=shop.models.upload_shop_interior_path)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_interior', to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShopPackagePromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pack_promotion_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('coupon_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promo_package', to='shop.shoppackage')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_promos', to='shop.shop')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='ShopPromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('level', models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Bronze', 'Bronze')], default='Gold', max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_promos', to='shop.shop')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='ShopService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('service_type', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_categories', to='shop.servicecategory')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_services', to='shop.shop')),
            ],
        ),
        migrations.AddField(
            model_name='shoppackage',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_service', to='shop.shopservice'),
        ),
        migrations.CreateModel(
            name='ShopStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('staff_name', models.CharField(blank=True, max_length=200, null=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('photo', models.ImageField(blank=True, default=shop.models.get_default_staff_image, null=True, upload_to=shop.models.upload_staff_photo_path)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_staffs', to='shop.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSpecialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_specialist', to='shop.shopservice')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_specialist', to='shop.shopstaff')),
            ],
        ),
        migrations.CreateModel(
            name='ShopVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visit_client', to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_visits', to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShopWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=shop.models.upload_shop_work_path)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_work', to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShopAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=9)),
                ('open', models.TimeField(blank=True, null=True)),
                ('closed', models.TimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_slots', to='shop.shop')),
            ],
            options={
                'unique_together': {('shop', 'day')},
            },
        ),
    ]

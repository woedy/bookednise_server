# Generated by Django 5.1 on 2024-11-27 06:40

import django.db.models.deletion
import user_profile.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True)),
                ('photo', models.ImageField(blank=True, default=user_profile.models.get_default_profile_image, null=True, upload_to=user_profile.models.upload_image_path)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('about_me', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=5000, null=True)),
                ('profile_complete', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('location_name', models.CharField(blank=True, max_length=200, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

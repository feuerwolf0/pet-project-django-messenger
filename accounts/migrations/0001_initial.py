# Generated by Django 5.0 on 2023-12-26 23:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=64, unique=True, verbose_name='Никнейм')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст')),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (0, 'Female')])),
                ('city', models.CharField(blank=True, max_length=64, null=True, verbose_name='Город проживания')),
                ('job', models.CharField(blank=True, max_length=64, null=True, verbose_name='Место работы')),
                ('about', models.TextField(blank=True, max_length=3072, null=True, verbose_name='О себе')),
                ('avatar', models.ImageField(blank=True, default='avatars/profile_default.jpg', null=True, upload_to='avatars/', verbose_name='Фото')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('is_banned', models.BooleanField(default=False, verbose_name='Забанен')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт')),
            ],
        ),
    ]

from django.db import models
from django.contrib.auth.models import User

GENDER_CHOISES = {
    1: 'Мужчина',
    0: 'Женщина'
}


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Аккаунт', related_name='account')
    username = models.CharField(max_length=64, verbose_name='Никнейм', unique=True)
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='E-mail', max_length=64, unique=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOISES)
    city = models.CharField(max_length=64, verbose_name='Город проживания', null=True, blank=True)
    job = models.CharField(max_length=64, verbose_name='Место работы', null=True, blank=True)
    about = models.TextField(max_length=3072, verbose_name='О себе', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Фото', null=True, blank=True,
                               default='avatars/profile_default.jpg')
    status = models.CharField(max_length=128, null=True, blank=True, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания', editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен', editable=False)
    is_banned = models.BooleanField(default=False, verbose_name='Забанен')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ('created_at', )

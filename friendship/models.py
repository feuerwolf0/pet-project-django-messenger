from django.contrib.auth.models import User
from django.db import models

from accounts.models import Account
from django.core.exceptions import ValidationError


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(Account,
                                  on_delete=models.CASCADE,
                                  related_name='friendship_request_sent')
    to_user = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                related_name='friendship_request_received')
    created_at = models.DateTimeField(auto_now_add=True)
    rejected_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Запрос в друзья'
        verbose_name_plural = 'Запросы в друзья'
        ordering = ['-created_at']

    def __str__(self):
        return f'Friendship Request: {self.from_user} -> {self.to_user}'

    def accept(self):
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

        self.delete()
        FriendshipRequest.objects.filter(from_user=self.to_user, to_user=self.from_user).delete()

        return True


class Friend(models.Model):
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friend_from')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friend_to')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f'Пользователь {self.from_user} дружит с {self.to_user}'

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError('Нельзя дружить самим с собой')
        return super()

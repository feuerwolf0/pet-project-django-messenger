from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import Account
from friendship.exceptions import FriendsDoesNotExist


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
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'
        ordering = ['-created_at']

    def __str__(self):
        return f'Запрос в друзья: {self.from_user} -> {self.to_user}'

    # Принять заявку в друзья
    def accept(self):
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)

        self.delete()
        FriendshipRequest.objects.filter(from_user=self.to_user, to_user=self.from_user).delete()

        return True

    # Отклонить заявку в друзья
    def reject(self):
        self.rejected_at = timezone.now()
        self.save()
        return True

    # Отменить заявку в друзья
    def cancel(self):
        self.delete()
        return True


class FriendManager(models.Manager):
    def friends(self, user):
        qs = super().prefetch_related('to_user').filter(from_user=user)
        qs |= super().prefetch_related('from_user').filter(to_user=user)

        friends = list()
        for u in qs:
            if u.to_user == user:
                friends.append(u.from_user)
            else:
                friends.append(u.to_user)
        return friends

    def are_friends(self, owner, profile):
        qs = super().filter(from_user__in=[owner, profile], to_user__in=[owner, profile])
        if not qs:
            return False
        return True

    def delete_friend(self, owner, profile):
        qs = super().filter(from_user__in=[owner, profile], to_user__in=[owner, profile])

        if not qs:
            raise FriendsDoesNotExist("Дружба не найдена")

        qs.delete()


class Friend(models.Model):
    from_user = models.ForeignKey(Account,
                                  on_delete=models.CASCADE,
                                  related_name='friend_from')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friend_to')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FriendManager()

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f'Пользователь {self.from_user} дружит с {self.to_user}'

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError('Нельзя дружить самим с собой')

        super().save(*args, **kwargs)

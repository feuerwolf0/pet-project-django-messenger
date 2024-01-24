from django.db.models.signals import post_save

from accounts.models import Account


def update_user_signal(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.email = instance.email
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.save()


post_save.connect(update_user_signal, sender=Account)

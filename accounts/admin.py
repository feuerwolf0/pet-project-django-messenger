from django.contrib import admin

from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_banned')
    list_filter = ('is_banned', )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'age', 'city')

from django.contrib import admin

from friendship.models import FriendshipRequest, Friend


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at', 'rejected_at')
    search_fields = ('from_user__username', 'to_user__username')


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')

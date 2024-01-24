from django.urls import path

from . import views

urlpatterns = [
    path('actions/friends/accept', views.accept_friendship, name='accept_friend'),
    path('actions/friends/reject', views.reject_friendship, name='reject_friend'),
    path('actions/friends/cancel', views.cancel_friendship, name='cancel_friend'),
    path('actions/friends/add', views.add_friend, name='add_friend'),
    path('actions/friends/delete', views.delete_friend, name='delete_friend'),
    path('profiles/<username>/', views.user_profile_view, name='user_profile'),
    path('myfriends/', views.myfriends_view, name='myfriends'),
    path('find_people/', views.PeopleView.as_view(), name='find_people')
]

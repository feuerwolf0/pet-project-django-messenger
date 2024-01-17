from django.urls import path

from . import views

urlpatterns = [
    path('profiles/<username>/add_friend/', views.add_friend, name='add_friend'),
    path('profiles/<username>/', views.user_profile_view, name='user_profile'),
    path('myfriends/', views.myfriends_view, name='myfriends'),
    path('find_people/', views.PeopleView.as_view(), name='find_people')
]

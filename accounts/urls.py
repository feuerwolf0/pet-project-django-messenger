from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/update_password/', views.update_password, name='update_password_profile'),
    path('profile/edit/change_password/', views.change_password_view, name='profile_change_password'),
    path('profile/edit/update_profile/', views.update_profile, name='update_profile'),
    path('profile/edit/upload_image/', views.profile_upload_image, name='profile_upload_image'),
    path('profile/edit', views.profile_edit_view, name='profile_edit'),
    path('profile/', views.profile_view, name='profile')
]

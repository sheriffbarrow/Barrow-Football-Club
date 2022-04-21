from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *



from . import views
app_name = 'account'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login-required/', views.login_view_required, name='login_required'),
    path('logout/', views.logout_view, name='logout'),
    path('update/', views.account_view, name='update'),
    path('post/history/', views.account_fitler, name='filter'),
    path('settings/', views.accountSettings, name='accountsettings'),
    path('settings/', views.account_view, name='settings'),
    path('registration/', views.registration, name='registration'),
]

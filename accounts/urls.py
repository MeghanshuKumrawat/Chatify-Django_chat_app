from django.urls import path
from .views import Sign_Up, Sign_In, Sign_Out, Settings

app_name = 'account'

urlpatterns = [
    path('sign-up', Sign_Up, name='sign-up'),
    path('sign-in', Sign_In, name='sign-in'),
    path('sign-out', Sign_Out, name='sign-out'),
    path('settings', Settings, name='settings'),
]

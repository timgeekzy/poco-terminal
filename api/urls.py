from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-token-info/', views.get_token_info, name='get_token_info'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.getExchange),
    path('getAPIExchange/', views.getAPIExchange)
]


from django.urls import path
from . import views

urlpatterns = [
    path('update/<int:pk>/', views.userUpdate),
]

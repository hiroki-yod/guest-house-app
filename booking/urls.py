from django.urls import path, include
from booking import views


urlpatterns = [
    path('', views.index, name='index'),
]
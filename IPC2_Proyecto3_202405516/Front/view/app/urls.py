from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enviar_configuracion/', views.enviar_configuracion, name='enviar_configuracion'),
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enviar_configuracion/', views.enviar_configuracion, name='enviar_configuracion'),
    path('enviar_consumos/', views.enviar_consumos, name='enviar_consumos'),
]
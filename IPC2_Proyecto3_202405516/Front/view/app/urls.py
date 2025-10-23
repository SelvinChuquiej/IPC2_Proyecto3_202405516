from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enviar_configuracion/', views.enviar_configuracion, name='enviar_configuracion'),
    path('enviar_consumos/', views.enviar_consumos, name='enviar_consumos'),
    path('consultar_datos/', views.consultar_datos, name='consultar_datos'),
    path('inicializar/', views.inicializar_sistema, name='inicializar_sistema'),
]
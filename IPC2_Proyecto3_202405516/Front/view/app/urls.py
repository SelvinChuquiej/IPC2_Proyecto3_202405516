from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enviar_configuracion/', views.enviar_configuracion, name='enviar_configuracion'),
    path('enviar_consumos/', views.enviar_consumos, name='enviar_consumos'),
    path('consultar_datos/', views.consultar_datos, name='consultar_datos'),
    path('inicializar/', views.inicializar_sistema, name='inicializar_sistema'),
    path('menu_creacion/', views.menu_creacion, name='menu_creacion'),
    path('menu_creacion/crear/categoria/', views.crear_categoria, name='crear_categoria'),
    path('menu_creacion/crear/recurso/', views.crear_recurso, name='crear_recurso'),
    path('menu_creacion/crear/configuracion/', views.crear_configuracion, name='crear_configuracion'),
]
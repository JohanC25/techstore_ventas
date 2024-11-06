from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('crear_venta/', views.crear_venta, name='crear_venta'),
    path('historial_ventas/', views.historial_ventas, name='historial_ventas'),
]

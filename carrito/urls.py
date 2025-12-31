from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('ver_repuestos/', views.ver_repuestos, name='ver_repuestos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:repuesto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/agregar_ajax/<int:repuesto_id>/', views.agregar_al_carrito_ajax, name='agregar_al_carrito_ajax'),
    path('carrito/detalle_ajax/', views.detalle_carrito_ajax, name='detalle_carrito_ajax'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/comprobante/', views.generar_comprobante, name='generar_comprobante'),
    path('mis_compras/', views.mis_compras, name='mis_compras'),
    path('detalle-compra/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
]

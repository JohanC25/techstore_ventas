from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Producto, Venta, Inventario
from .forms import VentaForm
from django.contrib import messages


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/lista_productos.html', {'productos': productos})


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto_id = form.cleaned_data['producto_id']  # Obtener el ID del producto seleccionado

            try:
                with transaction.atomic():
                    # Obtener el inventario y bloquear el registro
                    inventario = Inventario.objects.select_for_update().get(producto_id=producto_id)

                    if inventario.cantidad_disponible >= venta.cantidad_vendida:
                        inventario.cantidad_disponible -= venta.cantidad_vendida
                        inventario.save()
                        venta.producto_id = producto_id  # Asignar el ID del producto
                        venta.save()
                        messages.success(request, "Venta registrada con éxito.")
                        return redirect('historial_ventas')
                    else:
                        form.add_error('cantidad_vendida', 'Cantidad insuficiente en el inventario')
                        messages.error(request, "Cantidad insuficiente en el inventario.")
            except Inventario.DoesNotExist:
                messages.error(request, "El inventario para el producto no se encontró.")
                return redirect('lista_productos')
    else:
        form = VentaForm()
    return render(request, 'ventas/crear_venta.html', {'form': form})


def historial_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')

    # Crear un diccionario para mapear `producto_id` al `nombre` del producto
    producto_nombres = {producto.id: producto.nombre for producto in Producto.objects.all()}

    # Añadir el nombre del producto a cada venta en el contexto
    ventas_con_nombres = []
    for venta in ventas:
        venta_dict = {
            'producto_nombre': producto_nombres.get(venta.producto_id, "Producto desconocido"),
            'cantidad_vendida': venta.cantidad_vendida,
            'fecha_venta': venta.fecha_venta,
            'tienda_origen': venta.tienda_origen
        }
        ventas_con_nombres.append(venta_dict)

    return render(request, 'ventas/historial_ventas.html', {'ventas': ventas_con_nombres})

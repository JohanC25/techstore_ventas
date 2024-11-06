from django import forms
from .models import Venta
from django.db import connection


class VentaForm(forms.ModelForm):
    producto_id = forms.ChoiceField(label="Producto")

    class Meta:
        model = Venta
        fields = ['producto_id', 'cantidad_vendida', 'tienda_origen']

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        # Ejecutar una consulta directa para obtener los productos desde la tabla inventario_producto
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM inventario_producto")
            productos = cursor.fetchall()

        # Configurar el campo `producto_id` con los productos como opciones
        self.fields['producto_id'].choices = [(producto[0], producto[1]) for producto in productos]

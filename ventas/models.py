from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'inventario_producto'  # Apunta a la tabla existente en inventario

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='inventario')
    cantidad_disponible = models.IntegerField()
    ubicacion_tienda = models.CharField(max_length=255)
    estado_stock = models.CharField(max_length=50)

    class Meta:
        db_table = 'inventario_inventario'  # Apunta a la tabla existente en inventario

    def __str__(self):
        return f'{self.producto.nombre} - {self.ubicacion_tienda}'


class Venta(models.Model):
    producto_id = models.IntegerField()  # Guardamos el ID del producto sin clave foránea
    cantidad_vendida = models.IntegerField()
    fecha_venta = models.DateTimeField(auto_now_add=True)
    tienda_origen = models.CharField(max_length=255)

    class Meta:
        db_table = 'ventas_venta'  # Nos aseguramos de usar `ventas_venta`

    def __str__(self):
        return f'Venta de Producto ID {self.producto_id} - {self.cantidad_vendida} unidades'

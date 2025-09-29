from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    contrasena_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=30, unique=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.CharField(max_length=150, null=True, blank=True)
    condiciones_comerciales = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    unidad = models.CharField(max_length=50, null=True, blank=True)
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    id_receta = models.IntegerField(null=True, blank=True)  # BOM reference
    created_at = models.DateTimeField(auto_now_add=True)
    cantidad_producto = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Bodega(models.Model):
    id_bodega = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=255)
    capacidad = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    fecha_vencimiento = models.DateField()
    cantidad_inicial = models.IntegerField()
    cantidad_actual = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lote {self.id_lote} - {self.id_producto.nombre}"

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_bodega = models.ForeignKey(Bodega, on_delete=models.RESTRICT)
    id_lote = models.ForeignKey(Lote, on_delete=models.RESTRICT)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    id_usuario = models.IntegerField()  # Reference to Usuario
    updated_at_TIMESTAMP = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventario {self.id_producto.nombre} - {self.id_bodega.nombre}"

class Costo(models.Model):
    id_costo = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    tipo = models.CharField(max_length=100)  # ESTANDAR, REAL, PROMEDIO
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Costo {self.tipo} - {self.id_producto.nombre}"

class OrdenProduccion(models.Model):
    id_op = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50)
    cantidad_planificada = models.IntegerField()
    cantidad_real = models.IntegerField()
    merma = models.IntegerField()
    id_usuario = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OP {self.id_op} - {self.id_producto.nombre}"

class OrdenCompra(models.Model):
    id_oc = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.RESTRICT)
    fecha = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    id_usuario = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OC {self.id_oc} - {self.id_proveedor.nombre}"

class DetalleOC(models.Model):
    id_detalle_oc = models.AutoField(primary_key=True)
    id_oc = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.IntegerField()  # Reference to Cliente (not in diagram but needed)
    fecha = models.DateField()
    estado = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id_pedido}"

class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"
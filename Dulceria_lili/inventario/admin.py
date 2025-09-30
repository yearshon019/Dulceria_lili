from django.contrib import admin
from .models import (
    Proveedor, Producto, Bodega, Usuario, Lote, Inventario,
    Costo, OrdenCompra, DetalleOC, Pedido, DetallePedido, OrdenProduccion
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'nombre', 'email', 'rol', 'created_at']
    list_filter = ['rol', 'created_at']
    search_fields = ['nombre', 'email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id_proveedor', 'nombre', 'rut', 'contacto', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nombre', 'rut', 'contacto']
    ordering = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'nombre', 'unidad', 'precio_base', 'cantidad_producto', 'id_receta']
    list_filter = ['unidad', 'id_receta', 'created_at']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['id_bodega', 'nombre', 'ubicacion', 'capacidad', 'created_at']
    search_fields = ['nombre', 'ubicacion']
    ordering = ['nombre']

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['id_lote', 'id_producto', 'fecha_vencimiento', 'cantidad_inicial', 'cantidad_actual', 'created_at']
    list_filter = ['fecha_vencimiento', 'id_producto', 'created_at']
    search_fields = ['id_producto__nombre']
    ordering = ['-fecha_vencimiento']
    date_hierarchy = 'fecha_vencimiento'

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['id_inventario', 'id_producto', 'id_bodega', 'id_lote', 'id_usuario', 'updated_at_TIMESTAMP']
    list_filter = ['id_bodega', 'id_producto', 'updated_at_TIMESTAMP']
    search_fields = ['id_producto__nombre', 'id_bodega__nombre']
    ordering = ['-updated_at_TIMESTAMP']
    date_hierarchy = 'updated_at_TIMESTAMP'

@admin.register(Costo)
class CostoAdmin(admin.ModelAdmin):
    list_display = ['id_costo', 'id_producto', 'tipo', 'valor', 'fecha', 'created_at']
    list_filter = ['tipo', 'fecha', 'created_at']
    search_fields = ['id_producto__nombre', 'tipo']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id_oc', 'id_proveedor', 'fecha', 'estado', 'total', 'created_at']
    list_filter = ['estado', 'fecha', 'created_at']
    search_fields = ['id_proveedor__nombre']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'

class DetalleOCInline(admin.TabularInline):
    model = DetalleOC
    extra = 0

@admin.register(DetalleOC)
class DetalleOCAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_oc', 'id_oc', 'id_producto', 'cantidad', 'precio', 'created_at']
    list_filter = ['created_at']
    search_fields = ['id_oc__id_oc', 'id_producto__nombre']
    ordering = ['-created_at']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'id_cliente', 'fecha', 'estado', 'total', 'created_at']
    list_filter = ['estado', 'fecha', 'created_at']
    search_fields = ['id_pedido', 'id_cliente']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_pedido', 'id_pedido', 'id_producto', 'cantidad', 'precio', 'created_at']
    list_filter = ['created_at']
    search_fields = ['id_pedido__id_pedido', 'id_producto__nombre']
    ordering = ['-created_at']

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ['id_op', 'id_producto', 'fecha_inicio', 'fecha_fin', 'estado', 'cantidad_planificada', 'cantidad_real', 'merma']
    list_filter = ['estado', 'fecha_inicio', 'fecha_fin']
    search_fields = ['id_producto__nombre']
    ordering = ['-fecha_inicio']
    date_hierarchy = 'fecha_inicio'

# Mejorar el admin de OrdenCompra con inline de detalles
OrdenCompraAdmin.inlines = [DetalleOCInline]

# Mejorar el admin de Pedido con inline de detalles  
PedidoAdmin.inlines = [DetallePedidoInline]
from django.core.management.base import BaseCommand
from inventario.models import (
    Proveedor, Producto, Bodega, Usuario, Lote, Inventario, 
    Costo, OrdenCompra, DetalleOC, Pedido, DetallePedido, OrdenProduccion
)
from datetime import date, datetime
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Carga datos de ejemplo para Dulcería Lilis según diagrama aprobado"
    
    def handle(self, *args, **kwargs):
        # 1. Usuarios (según roles del sistema ERP)
        usuario_compras, created = Usuario.objects.get_or_create(
            nombre="Operador Compras",
            defaults={
                "email": "compras@lilis.cl",
                "rol": "Operador de Compras",
                "contrasena_hash": make_password("compras123")
            }
        )
        if created:
            self.stdout.write(f"✅ Usuario creado: {usuario_compras.nombre}")
        
        usuario_produccion, created = Usuario.objects.get_or_create(
            nombre="Jefe Producción",
            defaults={
                "email": "produccion@lilis.cl", 
                "rol": "Operador de Producción",
                "contrasena_hash": make_password("produccion123")
            }
        )
        if created:
            self.stdout.write(f"✅ Usuario creado: {usuario_produccion.nombre}")
        
        # 2. Proveedores
        prov_papaya, created = Proveedor.objects.get_or_create(
            rut="12345678-9",
            defaults={
                "nombre": "Agrícola Papaya Local",
                "direccion": "Valle del Elqui, La Serena",
                "contacto": "contacto@papayalocal.cl",
                "condiciones_comerciales": "Pago 30 días, entrega semanal"
            }
        )
        if created:
            self.stdout.write(f"✅ Proveedor creado: {prov_papaya.nombre}")
        
        prov_insumos, created = Proveedor.objects.get_or_create(
            rut="98765432-1",
            defaults={
                "nombre": "Distribuidora Insumos Norte",
                "direccion": "Coquimbo, Región de Coquimbo",
                "contacto": "ventas@insumosnorte.cl",
                "condiciones_comerciales": "Pago al contado, descuento por volumen"
            }
        )
        if created:
            self.stdout.write(f"✅ Proveedor creado: {prov_insumos.nombre}")
        
        # 3. Bodegas
        bodega_mp, created = Bodega.objects.get_or_create(
            nombre="Bodega Materias Primas",
            defaults={
                "ubicacion": "Planta Principal - Área A",
                "capacidad": 1000
            }
        )
        if created:
            self.stdout.write(f"✅ Bodega creada: {bodega_mp.nombre}")
        
        bodega_pt, created = Bodega.objects.get_or_create(
            nombre="Bodega Productos Terminados",
            defaults={
                "ubicacion": "Planta Principal - Área B", 
                "capacidad": 500
            }
        )
        if created:
            self.stdout.write(f"✅ Bodega creada: {bodega_pt.nombre}")
        
        # 4. Productos
        # Materias primas
        papaya_deshidratada, created = Producto.objects.get_or_create(
            nombre="Papaya Deshidratada Regional",
            defaults={
                "descripcion": "Papaya del Valle del Elqui para alfajores",
                "unidad": "kg",
                "precio_base": 8500.00,
                "id_receta": None,
                "cantidad_producto": 100
            }
        )
        if created:
            self.stdout.write(f"✅ Producto creado: {papaya_deshidratada.nombre}")
        
        # Productos terminados
        alfajor_papaya, created = Producto.objects.get_or_create(
            nombre="Alfajor de Papaya Artesanal",
            defaults={
                "descripcion": "Alfajor único en el mercado chileno",
                "unidad": "unidad",
                "precio_base": 1500.00,
                "id_receta": 1,
                "cantidad_producto": 500
            }
        )
        if created:
            self.stdout.write(f"✅ Producto creado: {alfajor_papaya.nombre}")
        
        alfajor_chocolate, created = Producto.objects.get_or_create(
            nombre="Alfajor Chocolate Premium",
            defaults={
                "descripcion": "Alfajor artesanal con chocolate negro/blanco",
                "unidad": "unidad",
                "precio_base": 1200.00,
                "id_receta": 2,
                "cantidad_producto": 300
            }
        )
        if created:
            self.stdout.write(f"✅ Producto creado: {alfajor_chocolate.nombre}")
        
        # 5. Lotes para trazabilidad
        lote_papaya, created = Lote.objects.get_or_create(
            id_producto=papaya_deshidratada,
            fecha_vencimiento=date(2025, 12, 31),
            defaults={
                "cantidad_inicial": 100,
                "cantidad_actual": 80
            }
        )
        if created:
            self.stdout.write(f"✅ Lote creado: {lote_papaya}")
        
        # 6. Inventario inicial
        inventario, created = Inventario.objects.get_or_create(
            id_producto=papaya_deshidratada,
            id_bodega=bodega_mp,
            id_lote=lote_papaya,
            defaults={
                "id_usuario": usuario_compras.id_usuario
            }
        )
        if created:
            self.stdout.write(f"✅ Inventario creado: {inventario}")
        
        # 7. Costos estándar
        costo, created = Costo.objects.get_or_create(
            id_producto=alfajor_papaya,
            tipo="ESTANDAR",
            fecha=date.today(),
            defaults={
                "valor": 950.00
            }
        )
        if created:
            self.stdout.write(f"✅ Costo creado: {costo}")
        
        # 8. Orden de compra inicial
        orden_compra, created = OrdenCompra.objects.get_or_create(
            id_proveedor=prov_papaya,
            fecha=date.today(),
            defaults={
                "estado": "PENDIENTE",
                "total": 85000.00,
                "id_usuario": usuario_compras.id_usuario
            }
        )
        if created:
            self.stdout.write(f"✅ Orden de compra creada: {orden_compra}")
        
        # 9. Detalle de orden de compra
        detalle_oc, created = DetalleOC.objects.get_or_create(
            id_oc=orden_compra,
            id_producto=papaya_deshidratada,
            defaults={
                "cantidad": 10,
                "precio": 8500.00
            }
        )
        if created:
            self.stdout.write(f"✅ Detalle OC creado: {detalle_oc}")
        
        # 10. Pedido de cliente (retail)
        pedido_unimarc, created = Pedido.objects.get_or_create(
            id_cliente=1,  # Cliente Unimarc 
            fecha=date.today(),
            defaults={
                "estado": "CONFIRMADO",
                "total": 450000.00
            }
        )
        if created:
            self.stdout.write(f"✅ Pedido creado: {pedido_unimarc}")
        
        # 11. Detalle de pedido
        detalle_pedido, created = DetallePedido.objects.get_or_create(
            id_pedido=pedido_unimarc,
            id_producto=alfajor_papaya,
            defaults={
                "cantidad": 300,
                "precio": 1500.00
            }
        )
        if created:
            self.stdout.write(f"✅ Detalle pedido creado: {detalle_pedido}")
        
        # 12. Orden de producción
        orden_prod, created = OrdenProduccion.objects.get_or_create(
            id_producto=alfajor_papaya,
            fecha_inicio=date.today(),
            defaults={
                "fecha_fin": None,
                "estado": "EN_PROCESO",
                "cantidad_planificada": 300,
                "cantidad_real": 0,
                "merma": 0,
                "id_usuario": usuario_produccion.id_usuario
            }
        )
        if created:
            self.stdout.write(f"✅ Orden de producción creada: {orden_prod}")
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Datos completos de Dulcería Lilis cargados según diagrama aprobado')
        )
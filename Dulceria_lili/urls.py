from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import LoginForm
from core.views import dashboard
from inventario import views as inv_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN / LOGOUT
    path('dulceria_lili/login/', LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True
    ), name='login'),

    path('dulceria_lili/logout/', LogoutView.as_view(), name='logout'),

    # DASHBOARD
    path('dulceria_lili/', dashboard, name='dashboard'),

    # PRODUCTOS
    path('dulceria_lili/productos/', inv_views.ProductoListView.as_view(), name='producto_list'),
    path('dulceria_lili/productos/create/', inv_views.ProductoCreateView.as_view(), name='producto_create'),
    path('dulceria_lili/productos/<int:pk>/update/', inv_views.ProductoUpdateView.as_view(), name='producto_update'),
    path('dulceria_lili/productos/<int:pk>/delete/', inv_views.ProductoDeleteView.as_view(), name='producto_delete'),

    # PROVEEDORES
    path('dulceria_lili/proveedores/', inv_views.ProveedorListView.as_view(), name='proveedor_list'),
    path('dulceria_lili/proveedores/create/', inv_views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('dulceria_lili/proveedores/<int:pk>/update/', inv_views.ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('dulceria_lili/proveedores/<int:pk>/delete/', inv_views.ProveedorDeleteView.as_view(), name='proveedor_delete'),

    # ORDENES DE COMPRA
    path('dulceria_lili/ordenes/', inv_views.OrdenCompraListView.as_view(), name='orden_list'),
    path('dulceria_lili/ordenes/create/', inv_views.OrdenCompraCreateView.as_view(), name='orden_create'),
    path('dulceria_lili/ordenes/<int:pk>/', inv_views.OrdenCompraDetailView.as_view(), name='orden_detail'),

    # Redirección de raíz
    path('', dashboard),
]

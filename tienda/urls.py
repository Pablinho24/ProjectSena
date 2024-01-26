from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('inicio/', views.inicio, name="inicio"),

	# Autenticación de usuarios del sistema
	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),
    path('perfil/', views.perfil, name="perfil"),
    path('cambioclave/', views.cambioclave, name="cambioclave"),
    path("cambiar_clave/", views.cambiar_clave, name="cambiar_clave"),


	# CRUD de Categorías
	path("categorias_listar/", views.categorias, name="categorias_listar"),
	path("categorias_form/", views.categorias_form, name="categorias_form"),
	path("categorias_crear/", views.categorias_crear, name="categorias_crear"),
	path("categorias_eliminar/<int:id>", views.categorias_eliminar, name="categorias_eliminar"),
	path("categorias_formulario_editar/<int:id>", views.categorias_formulario_editar, name="categorias_formulario_editar"),
	path("categorias_actualizar/", views.categorias_actualizar, name="categorias_actualizar"),

	# CRUD de Productos
	path("productos_listar/", views.productos, name="productos_listar"),
	path("productos_form/", views.productos_form, name="productos_form"),
	path("productos_crear/", views.productos_crear, name="productos_crear"),
	path("productos_eliminar/<int:id>", views.productos_eliminar, name="productos_eliminar"),
	path("productos_formulario_editar/<int:id>", views.productos_formulario_editar, name="productos_formulario_editar"),
	path("productos_actualizar/", views.productos_actualizar, name="productos_actualizar"),
]

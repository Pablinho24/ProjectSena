from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

# Importamos todos los modelos de la base de datos
from .models import *

# Create your views here.

def index(request):
	logueo = request.session.get("logueo", False)

	if logueo == False:
		return render(request, "tienda/login/login.html")
	else:
		return redirect("inicio")
	

def perfil(request):
	logueo = request.session.get("logueo", False)
	#Consultamos en Base de Datos por el ID del usuarioi logueado.
	q = Usuario.objects.get(pk = logueo["id"])
	contexto = {"data": q}
	return render(request, "tienda/login/perfil.html", contexto)

def cambioclave(request):
	return render(request, "tienda/login/cambioclave.html")


def cambiar_clave(request):
	if request.method == "POST":
		logueo = request.session.get("logueo", False)
		q = Usuario.objects.get(pk = logueo["id"])

		c1 = request.POST.get("nueva1")
		c2 = request.POST.get("nueva2")


		if q.clave == request.POST.get("clave"):
			if c1 == c2:
				#Cambiar clave en Base de Datos.
				q.clave = c1
				q.save()
				messages.success(request, "Contraseña guardada correctamente")
				#redirect("cambioclave")
			else:
				messages.info(request, "Las contraseñas nuevas no coinciden")
				#redirect("cambioclave")
		else:
			messages.error(request, "Contraseña no válida...")
			#redirect("cambioclave")
	else:
		messages.warning(request, "Error: no se enviaron datos..")

	return redirect("cambioclave")


	


def login(request):
	if request.method == "POST":
		user = request.POST.get("correo")
		passw = request.POST.get("clave")
		# select * from Usuario where correo = "user" and clave = "passw"
		try:
			q = Usuario.objects.get(correo=user, clave=passw)
			# Crear variable de sesión
			request.session["logueo"] = {
				"id": q.id,
				"nombre": q.nombre,
				"rol": q.rol,
				"nombre_rol": q.get_rol_display()
			}
			messages.success(request, f"Bienvenido {q.nombre}!!")
			return redirect("inicio")
		except Exception as e:
			messages.error(request, "Error: Usuario o contraseña incorrectos...")
			return redirect("index")
	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("index")


def logout(request):
	try:
		del request.session["logueo"]
		messages.success(request, "Sesión cerrada correctamente!")
		return redirect("index")
	except Exception as e:
		messages.warning(request, "No se pudo cerrar sesión...")
		return redirect("inicio")


def inicio(request):
	logueo = request.session.get("logueo", False)

	if logueo:
		categorias = Categoria.objects.all()

		cat = request.GET.get("cat")
		if cat == None:
			productos = Producto.objects.all()
		else:
			c = Categoria.objects.get(pk=cat)
			productos = Producto.objects.filter(categoria=c)

		contexto = {"data": productos, "cat":categorias}
		return render(request, "tienda/inicio.html", contexto)

	else:
		return redirect("index")


from .decorador_especial import *


@login_requerido
def categorias(request):
	q = Categoria.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias.html", contexto)



def categorias_form(request):
	return render(request, "tienda/categorias/categorias_form.html")


def categorias_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")
		try:
			q = Categoria(
				nombre=nomb,
				descripcion=desc
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("categorias_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("categorias_listar")


def categorias_eliminar(request, id):
	try:
		q = Categoria.objects.get(pk=id)
		q.delete()
		messages.success(request, "Categoría eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("categorias_listar")


def categorias_formulario_editar(request, id):
	q = Categoria.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias_formulario_editar.html", contexto)

def categorias_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")
		try:
			q = Categoria.objects.get(pk=id)
			q.nombre = nomb
			q.descripcion = desc
			q.save()
			messages.success(request, "Categoría actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("categorias_listar")


@login_requerido
def productos(request):
	q = Producto.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos.html", contexto)


def productos_form(request):
	q = Categoria.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos_form.html", contexto)


def productos_crear(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = Categoria.objects.get(pk=request.POST.get("categoria"))
		try:
			q = Producto(
				nombre=nombre,
				precio=precio,
				inventario=inventario,
				fecha_creacion=fecha_creacion,
				categoria=categoria
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("productos_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("productos_listar")


def productos_eliminar(request, id):
	try:
		q = Producto.objects.get(pk=id)
		q.delete()
		messages.success(request, "Producto eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("productos_listar")


def productos_formulario_editar(request, id):
	q = Producto.objects.get(pk=id)
	c = Categoria.objects.all()
	contexto = {"data": q, "categoria": c}
	return render(request, "tienda/productos/productos_formulario_editar.html", contexto)

def productos_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = Categoria.objects.get(pk=request.POST.get("categoria"))
		try:
			q = Producto.objects.get(pk=id)
			q.nombre = nombre
			q.precio = precio
			q.inventario = inventario
			q.fecha_creacion = fecha_creacion
			q.categoria = categoria
			q.save()
			messages.success(request, "Producto actualizado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("productos_listar")


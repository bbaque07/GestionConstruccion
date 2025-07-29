# services/proveedor_service.py
from repositories.proveedor_repository import (
    insertar_proveedor,
    obtener_todos_proveedores,
    obtener_proveedor_db,
    actualizar_proveedor_db,
    eliminar_proveedor_db,
    proveedor_tiene_materiales
)
from services.bitacora_service import registrar_bitacora

def crear_proveedor(nombre, contacto, telefono, direccion, ciudad, ruc, usuario):
    insertar_proveedor(nombre, contacto, telefono, direccion, ciudad, ruc)
    registrar_bitacora(usuario, "proveedores", "crear", f"Creó proveedor '{nombre}'")

def listar_proveedores():
    return obtener_todos_proveedores()

def obtener_proveedor_por_id(id):
    return obtener_proveedor_db(id)

def actualizar_proveedor(id, nombre, contacto, telefono, direccion, ciudad, ruc, usuario):
    actualizar_proveedor_db(id, nombre, contacto, telefono, direccion, ciudad, ruc)
    registrar_bitacora(usuario, "proveedores", "actualizar", f"Actualizó proveedor {id}")

def eliminar_proveedor(id, nombre, usuario):
    if proveedor_tiene_materiales(id):
        return False
    eliminar_proveedor_db(id)
    registrar_bitacora(usuario, "proveedores", "eliminar", f"Eliminó proveedor '{nombre}' id={id}")
    return True

# controllers/proveedor_controller.py
import streamlit as st
from services.proveedor_service import (
    crear_proveedor,
    listar_proveedores,
    obtener_proveedor_por_id,
    actualizar_proveedor,
    eliminar_proveedor
)

def crear_proveedor_controller(nombre, contacto, telefono, direccion, ciudad, ruc):
    usuario = obtener_usuario_actual()
    crear_proveedor(nombre, contacto, telefono, direccion, ciudad, ruc, usuario)

def listar_proveedores_controller():
    return listar_proveedores()

def obtener_proveedor_controller(id):
    return obtener_proveedor_por_id(id)

def actualizar_proveedor_controller(id, nombre, contacto, telefono, direccion, ciudad, ruc):
    usuario = obtener_usuario_actual()
    actualizar_proveedor(id, nombre, contacto, telefono, direccion, ciudad, ruc, usuario)

def eliminar_proveedor_controller(id, nombre):
    usuario = obtener_usuario_actual()
    return eliminar_proveedor(id, nombre, usuario)

def obtener_usuario_actual():
    return (
        st.session_state["usuario"]["usuario"]
        if "usuario" in st.session_state
        else "desconocido"
    )

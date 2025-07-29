from repositories.clientes_repository import (
    crear_cliente, obtener_todos_los_clientes, obtener_cliente_por_id,
    actualizar_cliente, eliminar_cliente, cliente_esta_en_proyectos
)
from services.bitacora_service import registrar_bitacora
import streamlit as st

def crear_cliente_service(nombre, contacto, telefono, direccion, ciudad, ruc):
    crear_cliente(nombre, contacto, telefono, direccion, ciudad, ruc)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="clientes",
        tipo_accion="crear",
        descripcion=f"Creó cliente '{nombre}' (contacto={contacto}, tel={telefono}, ciudad={ciudad})"
    )

def actualizar_cliente_service(cliente_id, nombre, contacto, telefono, direccion, ciudad, ruc):
    actualizar_cliente(cliente_id, nombre, contacto, telefono, direccion, ciudad, ruc)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="clientes",
        tipo_accion="actualizar",
        descripcion=f"Actualizó cliente id={cliente_id}: nombre={nombre}, contacto={contacto}, telefono={telefono}, direccion={direccion}, ciudad={ciudad}, ruc={ruc}"
    )

def eliminar_cliente_service(cliente_id, nombre_cliente):
    if cliente_esta_en_proyectos(cliente_id):
        return False, "No puedes eliminar este cliente porque está asociado a uno o más proyectos."
    eliminar_cliente(cliente_id)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="clientes",
        tipo_accion="eliminar",
        descripcion=f"Eliminó cliente '{nombre_cliente}' con id={cliente_id}"
    )
    return True, f"Cliente {nombre_cliente} eliminado."

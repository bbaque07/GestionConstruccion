from repositories.proyectos_repository import (
    obtener_todos_proyectos, crear_nuevo_proyecto,
    actualizar_proyecto_db, eliminar_proyecto_db,
    proyecto_en_uso, buscar_proyecto_por_id
)
from services.bitacora_service import registrar_bitacora
import streamlit as st

def listar_proyectos():
    return obtener_todos_proyectos()

def insertar_proyecto(nombre, descripcion, fecha_inicio, fecha_fin, cliente_id):
    crear_nuevo_proyecto(nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="proyectos",
        tipo_accion="crear",
        descripcion=f"Creó proyecto '{nombre}' ({descripcion}, {fecha_inicio} a {fecha_fin}, cliente_id={cliente_id})"
    )

def editar_proyecto(id, nombre, descripcion, fecha_inicio, fecha_fin, cliente_id):
    actualizar_proyecto_db(id, nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="proyectos",
        tipo_accion="actualizar",
        descripcion=f"Actualizó proyecto id={id}: {nombre}, {descripcion}, {fecha_inicio} a {fecha_fin}, cliente_id={cliente_id}"
    )

def borrar_proyecto(id, nombre):
    if proyecto_en_uso(id):
        return False
    eliminar_proyecto_db(id)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="proyectos",
        tipo_accion="eliminar",
        descripcion=f"Eliminó proyecto '{nombre}' con id={id}"
    )
    return True

def get_proyecto_por_id(id):
    return buscar_proyecto_por_id(id)

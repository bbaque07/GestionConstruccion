import streamlit as st
from repositories.materiales_repository import (
    insertar_material,
    obtener_todos_los_materiales,
    obtener_material_por_id_db,
    actualizar_material_db,
    eliminar_material_db,
    verificar_relacion_material
)
from services.bitacora_service import registrar_bitacora

def crear_material(nombre, unidad, stock, precio):
    if not nombre:
        st.error("El nombre es obligatorio.")
        return
    insertar_material(nombre, unidad, stock, precio)
    
    st.success("Material registrado correctamente.")
    st.rerun()


def obtener_materiales():
    return obtener_todos_los_materiales()


def obtener_material_por_id(id_):
    return obtener_material_por_id_db(id_)


def actualizar_material(id_, nombre, unidad, stock, precio):
    actualizar_material_db(id_, nombre, unidad, stock, precio)
    
    st.success("Material actualizado.")
    st.session_state["editando_material_id"] = None
    st.rerun()


def eliminar_material(id_):
    if verificar_relacion_material(id_):
        st.error("No puedes eliminar este material porque está asociado a uno o más proyectos.")
        return
    material = obtener_material_por_id(id_)
    eliminar_material_db(id_)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="materiales",
        tipo_accion="eliminar",
        descripcion=f"Eliminó material '{material['nombre']}' con id={id_}"
    )
    st.success(f"Material {material['nombre']} eliminado.")

import streamlit as st
from views.materiales_view import (
    formulario_creacion_material,
    formulario_edicion_material,
    mostrar_materiales
)
from services.materiales_service import (
    crear_material,
    obtener_materiales,
    obtener_material_por_id,
    actualizar_material,
    eliminar_material
)

def crud_materiales(permisos="admin"):
    st.title("CRUD de Materiales")
    st.markdown("---")

    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    if "editando_material_id" not in st.session_state:
        st.session_state["editando_material_id"] = None
    if "eliminando_material_id" not in st.session_state:
        st.session_state["eliminando_material_id"] = None

    # Eliminar
    if st.session_state["eliminando_material_id"]:
        eliminar_material(st.session_state["eliminando_material_id"])
        st.session_state["eliminando_material_id"] = None
        st.rerun()

    # Editar
    elif st.session_state["editando_material_id"]:
        material = obtener_material_por_id(st.session_state["editando_material_id"])
        if material:
            formulario_edicion_material(
                material,
                callback_actualizar=lambda nombre, unidad, stock, precio:
                    actualizar_material(material["id"], nombre, unidad, stock, precio),
                callback_cancelar=lambda: cancelar_edicion()
            )
    else:
        if permisos in ("admin", "usuario"):
            formulario_creacion_material(crear_material)
    
    # Mostrar lista
    materiales = obtener_materiales()
    mostrar_materiales(materiales, permisos)

def cancelar_edicion():
    st.session_state["editando_material_id"] = None
    st.rerun()

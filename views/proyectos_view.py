import streamlit as st
from controllers.proyectos_controller import (
    obtener_proyectos, crear_proyecto, actualizar_proyecto,
    eliminar_proyecto, obtener_proyecto_por_id
)

def vista_crud_proyectos(permisos="admin"):
    st.title("CRUD de Proyectos")
    st.markdown("---")

    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    if "editando_proyecto_id" not in st.session_state:
        st.session_state["editando_proyecto_id"] = None

    if st.session_state["editando_proyecto_id"]:
        proyecto = obtener_proyecto_por_id(st.session_state["editando_proyecto_id"])
        if proyecto:
            nombre = st.text_input("Nombre", value=proyecto["nombre"], key="proyecto_nombre_edit")
            descripcion = st.text_area("Descripción", value=proyecto["descripcion"], key="proyecto_desc_edit")
            fecha_inicio = st.date_input("Fecha de inicio", value=proyecto["fecha_inicio"], key="proyecto_ini_edit")
            fecha_fin = st.date_input("Fecha de fin", value=proyecto["fecha_fin"], key="proyecto_fin_edit")
            cliente_id = st.number_input("ID Cliente", min_value=1, value=proyecto["cliente_id"] or 1, key="proyecto_cliente_edit")

            if permisos in ("admin", "usuario") and st.button("Actualizar"):
                actualizar_proyecto(proyecto["id"], nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)
                st.success("Proyecto actualizado.")
                st.session_state["editando_proyecto_id"] = None
                st.rerun()

            if st.button("Cancelar edición"):
                st.session_state["editando_proyecto_id"] = None
                st.rerun()
    else:
        if permisos in ("admin", "usuario"):
            with st.form("form_nuevo_proyecto"):
                nombre = st.text_input("Nombre", key="proyecto_nombre")
                descripcion = st.text_area("Descripción", key="proyecto_desc")
                fecha_inicio = st.date_input("Fecha de inicio", key="proyecto_ini")
                fecha_fin = st.date_input("Fecha de fin", key="proyecto_fin")
                cliente_id = st.number_input("ID Cliente", min_value=1, key="proyecto_cliente")

                if st.form_submit_button("Guardar"):
                    if nombre:
                        crear_proyecto(nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)
                        st.success("Proyecto registrado correctamente.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

    proyectos = obtener_proyectos()
    st.write("Listado de proyectos:")
    for _, row in proyectos.iterrows():
        cols = st.columns([1, 2, 2, 2, 2, 2, 1, 1])
        cols[0].write(row["id"])
        cols[1].write(row["nombre"])
        cols[2].write(row["descripcion"])
        cols[3].write(row["fecha_inicio"])
        cols[4].write(row["fecha_fin"])
        cols[5].write(row["cliente_id"])
        if permisos in ("admin", "usuario"):
            if cols[6].button("✏️", key=f"edit_proyecto_{row['id']}"):
                st.session_state["editando_proyecto_id"] = int(row["id"])
                st.rerun()
        else:
            cols[6].write("-")
        if permisos == "admin":
            if cols[7].button("🗑️", key=f"del_proyecto_{row['id']}"):
                eliminado = eliminar_proyecto(row["id"], row["nombre"])
                if eliminado:
                    st.success(f"Proyecto {row['nombre']} eliminado.")
                    st.rerun()
                else:
                    st.error("No puedes eliminar este proyecto porque está asociado a materiales.")
        else:
            cols[7].write("-")

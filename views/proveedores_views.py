# views/proveedores_views.py
import streamlit as st
from controllers.proveedor_controller import (
    crear_proveedor_controller,
    listar_proveedores_controller,
    actualizar_proveedor_controller,
    eliminar_proveedor_controller,
    obtener_proveedor_controller
)

def crud_proveedores(permisos="admin"):
    st.title("CRUD de Proveedores")
    st.markdown("---")

    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    if "editando_prov_id" not in st.session_state:
        st.session_state["editando_prov_id"] = None

    if st.session_state["editando_prov_id"]:
        proveedor = obtener_proveedor_controller(st.session_state["editando_prov_id"])
        if proveedor:
            nombre = st.text_input("Nombre", value=proveedor["nombre"])
            contacto = st.text_input("Contacto", value=proveedor["contacto"])
            telefono = st.text_input("Teléfono", value=proveedor["telefono"])
            direccion = st.text_input("Dirección", value=proveedor["direccion"])
            ciudad = st.text_input("Ciudad", value=proveedor["ciudad"])
            ruc = st.text_input("RUC", value=proveedor["ruc"])
            if st.button("Actualizar"):
                actualizar_proveedor_controller(
                    id=proveedor["id"], nombre=nombre, contacto=contacto,
                    telefono=telefono, direccion=direccion, ciudad=ciudad, ruc=ruc
                )
                st.success("Proveedor actualizado.")
                st.session_state["editando_prov_id"] = None
                st.rerun()
            if st.button("Cancelar edición"):
                st.session_state["editando_prov_id"] = None
                st.rerun()
    else:
        if permisos in ("admin", "usuario"):
            with st.form("form_nuevo_prov"):
                nombre = st.text_input("Nombre")
                contacto = st.text_input("Contacto")
                telefono = st.text_input("Teléfono")
                direccion = st.text_input("Dirección")
                ciudad = st.text_input("Ciudad")
                ruc = st.text_input("RUC")
                if st.form_submit_button("Guardar"):
                    if nombre:
                        crear_proveedor_controller(nombre, contacto, telefono, direccion, ciudad, ruc)
                        st.success("Proveedor registrado correctamente.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

    st.write("Listado de proveedores:")
    for prov in listar_proveedores_controller():
        cols = st.columns([1, 2, 2, 2, 2, 2, 2, 1, 1])
        cols[0].write(prov["id"])
        cols[1].write(prov["nombre"])
        cols[2].write(prov["contacto"])
        cols[3].write(prov["telefono"])
        cols[4].write(prov["direccion"])
        cols[5].write(prov["ciudad"])
        cols[6].write(prov["ruc"])
        if permisos in ("admin", "usuario"):
            if cols[7].button("✏️", key=f"edit_{prov['id']}"):
                st.session_state["editando_prov_id"] = prov["id"]
                st.rerun()
        else:
            cols[7].write("-")
        if permisos == "admin":
            if cols[8].button("🗑️", key=f"del_{prov['id']}"):
                eliminado = eliminar_proveedor_controller(prov["id"], prov["nombre"])
                if eliminado:
                    st.success(f"Proveedor {prov['nombre']} eliminado.")
                    st.rerun()
        else:
            cols[8].write("-")

import streamlit as st
from controllers.clientes_controller import (
    get_clientes, get_cliente_por_id, crear_cliente, 
    actualizar_cliente, eliminar_cliente
)

def mostrar_clientes(permisos="admin"):
    st.title("CRUD de Clientes")
    st.markdown("---")

    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    if "editando_cliente_id" not in st.session_state:
        st.session_state["editando_cliente_id"] = None

    if st.session_state["editando_cliente_id"]:
        cliente = get_cliente_por_id(st.session_state["editando_cliente_id"])
        if cliente is not None:
            nombre = st.text_input("Nombre", value=cliente["nombre"], key="cliente_nombre_edit")
            contacto = st.text_input("Contacto", value=cliente["contacto"], key="cliente_contacto_edit")
            telefono = st.text_input("Teléfono", value=cliente["telefono"], key="cliente_tel_edit")
            direccion = st.text_input("Dirección", value=cliente["direccion"], key="cliente_dir_edit")
            ciudad = st.text_input("Ciudad", value=cliente["ciudad"], key="cliente_ciudad_edit")
            ruc = st.text_input("RUC", value=cliente["ruc"], key="cliente_ruc_edit")
            if permisos in ("admin", "usuario"):
                if st.button("Actualizar"):
                    actualizar_cliente(cliente["id"], {
                        "nombre": nombre,
                        "contacto": contacto,
                        "telefono": telefono,
                        "direccion": direccion,
                        "ciudad": ciudad,
                        "ruc": ruc
                    })
                    st.success("Cliente actualizado.")
                    st.session_state["editando_cliente_id"] = None
                    st.rerun()
            if st.button("Cancelar edición"):
                st.session_state["editando_cliente_id"] = None
                st.rerun()
    else:
        if permisos in ("admin", "usuario"):
            with st.form("form_nuevo_cliente"):
                nombre = st.text_input("Nombre", key="cliente_nombre")
                contacto = st.text_input("Contacto", key="cliente_contacto")
                telefono = st.text_input("Teléfono", key="cliente_tel")
                direccion = st.text_input("Dirección", key="cliente_dir")
                ciudad = st.text_input("Ciudad", key="cliente_ciudad")
                ruc = st.text_input("RUC", key="cliente_ruc")
                if st.form_submit_button("Guardar"):
                    if nombre:
                        crear_cliente({
                            "nombre": nombre,
                            "contacto": contacto,
                            "telefono": telefono,
                            "direccion": direccion,
                            "ciudad": ciudad,
                            "ruc": ruc
                        })
                        st.success("Cliente registrado correctamente.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

    df = get_clientes()
    st.write("Listado de clientes:")
    for _, row in df.iterrows():
        cols = st.columns([1, 2, 2, 2, 2, 2, 2, 1, 1])
        cols[0].write(row["id"])
        cols[1].write(row["nombre"])
        cols[2].write(row["contacto"])
        cols[3].write(row["telefono"])
        cols[4].write(row["direccion"])
        cols[5].write(row["ciudad"])
        cols[6].write(row["ruc"])
        if permisos in ("admin", "usuario"):
            if cols[7].button("✏️", key=f"edit_cliente_{row['id']}"):
                st.session_state["editando_cliente_id"] = int(row["id"])
                st.rerun()
        else:
            cols[7].write("-")
        if permisos == "admin":
            if cols[8].button("🗑️", key=f"del_cliente_{row['id']}"):
                ok, msg = eliminar_cliente(row["id"], row["nombre"])
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            cols[8].write("-")

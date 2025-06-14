#providers_crud.py
import streamlit as st
import pandas as pd
from config import get_connection
from bitacora import registrar_bitacora   # Registro de acciones para la bitácora

def crud_proveedores(permisos="admin"):
    st.title("CRUD de Proveedores")
    st.markdown("---")

    # --- Control de permisos ---
    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    # --- Estado de edición ---
    if "editando_prov_id" not in st.session_state:
        st.session_state["editando_prov_id"] = None

    # --- Formulario de edición ---
    if st.session_state["editando_prov_id"]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM proveedores WHERE id=%s", (st.session_state["editando_prov_id"],))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            nombre = st.text_input("Nombre", value=row[1], key="prov_nombre_edit")
            contacto = st.text_input("Contacto", value=row[2], key="prov_contacto_edit")
            telefono = st.text_input("Teléfono", value=row[3], key="prov_tel_edit")
            direccion = st.text_input("Dirección", value=row[4], key="prov_dir_edit")
            ciudad = st.text_input("Ciudad", value=row[5], key="prov_ciudad_edit")
            ruc = st.text_input("RUC", value=row[6], key="prov_ruc_edit")
            if permisos in ("admin", "usuario"):
                if st.button("Actualizar"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE proveedores SET nombre=%s, contacto=%s, telefono=%s, direccion=%s, ciudad=%s, ruc=%s WHERE id=%s",
                        (nombre, contacto, telefono, direccion, ciudad, ruc, st.session_state["editando_prov_id"])
                    )
                    conn.commit()
                    # Auditoría
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="proveedores",
                        tipo_accion="actualizar",
                        descripcion=f"Actualizó proveedor id={st.session_state['editando_prov_id']}: nombre={nombre}, contacto={contacto}, telefono={telefono}, direccion={direccion}, ciudad={ciudad}, ruc={ruc}"
                    )
                    cur.close()
                    conn.close()
                    st.success("Proveedor actualizado.")
                    st.session_state["editando_prov_id"] = None
                    st.rerun()
            if st.button("Cancelar edición"):
                st.session_state["editando_prov_id"] = None
                st.rerun()

    # --- Formulario de nuevo proveedor ---
    else:
        if permisos in ("admin", "usuario"):
            with st.form("form_nuevo_prov"):
                nombre = st.text_input("Nombre", key="prov_nombre")
                contacto = st.text_input("Contacto", key="prov_contacto")
                telefono = st.text_input("Teléfono", key="prov_tel")
                direccion = st.text_input("Dirección", key="prov_dir")
                ciudad = st.text_input("Ciudad", key="prov_ciudad")
                ruc = st.text_input("RUC", key="prov_ruc")
                if st.form_submit_button("Guardar"):
                    if nombre:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO proveedores (nombre, contacto, telefono, direccion, ciudad, ruc) VALUES (%s, %s, %s, %s, %s, %s)",
                            (nombre, contacto, telefono, direccion, ciudad, ruc)
                        )
                        conn.commit()
                        # Auditoría
                        registrar_bitacora(
                            usuario=st.session_state["usuario"]["usuario"],
                            tabla="proveedores",
                            tipo_accion="crear",
                            descripcion=f"Creó proveedor '{nombre}' (contacto={contacto}, tel={telefono}, ciudad={ciudad})"
                        )
                        cur.close()
                        conn.close()
                        st.success("Proveedor registrado correctamente.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

    # --- Tabla de proveedores (listar, editar, eliminar) ---
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM proveedores ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    st.write("Listado de proveedores:")
    for row in rows:
        cols = st.columns([1, 2, 2, 2, 2, 2, 2, 1, 1])
        cols[0].write(row[0])  # id
        cols[1].write(row[1])  # nombre
        cols[2].write(row[2])  # contacto
        cols[3].write(row[3])  # telefono
        cols[4].write(row[4])  # direccion
        cols[5].write(row[5])  # ciudad
        cols[6].write(row[6])  # ruc
        # --- Editar
        if permisos in ("admin", "usuario"):
            if cols[7].button("✏️", key=f"edit_{row[0]}"):
                st.session_state["editando_prov_id"] = int(row[0])
                st.rerun()
        else:
            cols[7].write("-")
        # --- Eliminar solo admin y validación FK
        if permisos == "admin":
            if cols[8].button("🗑️", key=f"del_prov_{row[0]}"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM materiales_proyecto WHERE proveedor_id=%s", (int(row[0]),))
                cuenta = cur.fetchone()[0]
                if cuenta > 0:
                    st.error("No puedes eliminar este proveedor porque está asociado a uno o más materiales de proyectos.")
                else:
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="proveedores",
                        tipo_accion="eliminar",
                        descripcion=f"Eliminó proveedor '{row[1]}' con id={row[0]}"
                    )
                    cur.execute("DELETE FROM proveedores WHERE id=%s", (int(row[0]),))
                    conn.commit()
                    st.success(f"Proveedor {row[1]} eliminado.")
                    st.rerun()
                cur.close()
                conn.close()
        else:
            cols[8].write("-")
# Fin del CRUD de Proveedores
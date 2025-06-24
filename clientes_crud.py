#clientes_crud.py
import streamlit as st
import pandas as pd
from config import get_connection
from bitacora import registrar_bitacora   # Importa función de bitácora para auditoría

def crud_clientes(permisos="admin"):
    """
    Pantalla de gestión de clientes.
    - Admin: CRUD completo
    - Usuario: crear y actualizar
    - Invitado: sin acceso
    Todas las acciones se registran en la bitácora para auditoría.
    """
    st.title("CRUD de Clientes")
    st.markdown("---")

    # --- Verifica permisos ---
    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    # --- Modo edición: si hay cliente seleccionado para editar ---
    if "editando_cliente_id" not in st.session_state:
        st.session_state["editando_cliente_id"] = None
    if st.session_state["editando_cliente_id"]:
        # Obtiene los datos actuales del cliente
        conn = get_connection()
        df = pd.read_sql(
            "SELECT * FROM clientes WHERE id=%s",
            conn, params=(st.session_state["editando_cliente_id"],)
        )
        conn.close()
        if not df.empty:
            row = df.iloc[0]
            # Formulario de edición
            nombre = st.text_input("Nombre", value=row["nombre"], key="cliente_nombre_edit")
            contacto = st.text_input("Contacto", value=row["contacto"], key="cliente_contacto_edit")
            telefono = st.text_input("Teléfono", value=row["telefono"], key="cliente_tel_edit")
            direccion = st.text_input("Dirección", value=row["direccion"], key="cliente_dir_edit")
            ciudad = st.text_input("Ciudad", value=row["ciudad"], key="cliente_ciudad_edit")
            ruc = st.text_input("RUC", value=row["ruc"], key="cliente_ruc_edit")
            if permisos in ("admin", "usuario"):
                if st.button("Actualizar"):
                    # Actualiza en la base y registra en bitácora
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE clientes SET nombre=%s, contacto=%s, telefono=%s, direccion=%s, ciudad=%s, ruc=%s WHERE id=%s",
                        (nombre, contacto, telefono, direccion, ciudad, ruc, st.session_state["editando_cliente_id"])
                    )
                    conn.commit()
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="clientes",
                        tipo_accion="actualizar",
                        descripcion=f"Actualizó cliente id={st.session_state['editando_cliente_id']}: nombre={nombre}, contacto={contacto}, telefono={telefono}, direccion={direccion}, ciudad={ciudad}, ruc={ruc}"
                    )
                    cur.close()
                    conn.close()
                    st.success("Cliente actualizado.")
                    st.session_state["editando_cliente_id"] = None
                    st.rerun()
            if st.button("Cancelar edición"):
                st.session_state["editando_cliente_id"] = None
                st.rerun()
    else:
        # --- Modo creación de nuevo cliente ---
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
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO clientes (nombre, contacto, telefono, direccion, ciudad, ruc) VALUES (%s, %s, %s, %s, %s, %s)",
                            (nombre, contacto, telefono, direccion, ciudad, ruc)
                        )
                        conn.commit()
                        registrar_bitacora(
                            usuario=st.session_state["usuario"]["usuario"],
                            tabla="clientes",
                            tipo_accion="crear",
                            descripcion=f"Creó cliente '{nombre}' (contacto={contacto}, tel={telefono}, ciudad={ciudad})"
                        )
                        cur.close()
                        conn.close()
                        st.success("Cliente registrado correctamente.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

    # --- Listado y eliminación de clientes ---
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM clientes ORDER BY id desc", conn)
    conn.close()
    st.write("Listado de clientes:")
    for idx, row in df.iterrows():
        cols = st.columns([1, 2, 2, 2, 2, 2, 2, 1, 1])
        cols[0].write(row["id"])
        cols[1].write(row["nombre"])
        cols[2].write(row["contacto"])
        cols[3].write(row["telefono"])
        cols[4].write(row["direccion"])
        cols[5].write(row["ciudad"])
        cols[6].write(row["ruc"])
        # Solo admin y usuario pueden editar
        if permisos in ("admin", "usuario"):
            if cols[7].button("✏️", key=f"edit_cliente_{row['id']}"):
                st.session_state["editando_cliente_id"] = int(row["id"])
                st.rerun()
        else:
            cols[7].write("-")
        # Solo admin puede eliminar
        if permisos == "admin":
            if cols[8].button("🗑️", key=f"del_cliente_{row['id']}"):
                conn = get_connection()
                cur = conn.cursor()
                # Chequea FK: ¿está en proyectos?
                cur.execute("SELECT COUNT(*) FROM proyectos WHERE cliente_id=%s", (int(row["id"]),))
                cuenta = cur.fetchone()[0]
                if cuenta > 0:
                    st.error("No puedes eliminar este cliente porque está asociado a uno o más proyectos.")
                else:
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="clientes",
                        tipo_accion="eliminar",
                        descripcion=f"Eliminó cliente '{row['nombre']}' con id={row['id']}"
                    )
                    cur.execute("DELETE FROM clientes WHERE id=%s", (int(row["id"]),))
                    conn.commit()
                    st.success(f"Cliente {row['nombre']} eliminado.")
                    st.rerun()
                cur.close()
                conn.close()
        else:
            cols[8].write("-")

#materiales_crud.py
import streamlit as st
import pandas as pd
from config import get_connection
from bitacora import registrar_bitacora   # Importa función para registrar auditoría

def crud_materiales(permisos="admin"):
    """
    Pantalla de gestión de materiales.
    - Admin: CRUD completo
    - Usuario: crear y actualizar
    - Invitado: sin acceso
    Todas las acciones se registran en la bitácora para auditoría.
    """
    st.title("CRUD de Materiales")
    st.markdown("---")

    # --- Verifica permisos ---
    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    # --- Modo edición: si hay material seleccionado para editar ---
    if "editando_material_id" not in st.session_state:
        st.session_state["editando_material_id"] = None
    if st.session_state["editando_material_id"]:
        # Obtiene los datos actuales del material
        conn = get_connection()
        df = pd.read_sql(
            "SELECT * FROM materiales WHERE id=%s",
            conn, params=(st.session_state["editando_material_id"],)
        )
        conn.close()
        if not df.empty:
            row = df.iloc[0]
            # Formulario de edición
            nombre = st.text_input("Nombre", value=row["nombre"], key="material_nombre_edit")
            unidad = st.text_input("Unidad", value=row["unidad"], key="material_unidad_edit")
            stock = st.number_input("Stock", min_value=0, value=row["stock"], key="material_stock_edit")
            precio = st.number_input("Precio", min_value=0.0, value=float(row["precio"]), key="material_precio_edit")
            if permisos in ("admin", "usuario"):
                if st.button("Actualizar"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE materiales SET nombre=%s, unidad=%s, stock=%s, precio=%s WHERE id=%s",
                        (nombre, unidad, stock, precio, st.session_state["editando_material_id"])
                    )
                    conn.commit()
                    # REGISTRO EN BITÁCORA
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="materiales",
                        tipo_accion="actualizar",
                        descripcion=f"Actualizó material id={st.session_state['editando_material_id']}: nombre={nombre}, unidad={unidad}, stock={stock}, precio={precio}"
                    )
                    cur.close()
                    conn.close()
                    st.success("Material actualizado.")
                    st.session_state["editando_material_id"] = None
                    st.rerun()
            if st.button("Cancelar edición"):
                st.session_state["editando_material_id"] = None
                st.rerun()
    else:
        # --- Modo creación de nuevo material ---
        if permisos in ("admin", "usuario"):
            with st.form("form_nuevo_material"):
                nombre = st.text_input("Nombre", key="material_nombre")
                unidad = st.text_input("Unidad", key="material_unidad")
                stock = st.number_input("Stock", min_value=0, key="material_stock")
                precio = st.number_input("Precio", min_value=0.0, key="material_precio")
                if st.form_submit_button("Guardar"):
                    if nombre:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO materiales (nombre, unidad, stock, precio) VALUES (%s, %s, %s, %s)",
                            (nombre, unidad, stock, precio)
                        )
                        conn.commit()
                        # REGISTRO EN BITÁCORA
                        registrar_bitacora(
                            usuario=st.session_state["usuario"]["usuario"],
                            tabla="materiales",
                            tipo_accion="crear",
                            descripcion=f"Creó material '{nombre}' (unidad={unidad}, stock={stock}, precio={precio})"
                        )
                        cur.close()
                        conn.close()
                        st.success("Material registrado correctamente.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

    # --- Listado y eliminación de materiales ---
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM materiales ORDER BY id", conn)
    conn.close()
    st.write("Listado de materiales:")
    for idx, row in df.iterrows():
        cols = st.columns([1, 2, 2, 2, 2, 1, 1])
        cols[0].write(row["id"])
        cols[1].write(row["nombre"])
        cols[2].write(row["unidad"])
        cols[3].write(row["stock"])
        cols[4].write(row["precio"])
        # Solo admin y usuario pueden editar
        if permisos in ("admin", "usuario"):
            if cols[5].button("✏️", key=f"edit_material_{row['id']}"):
                st.session_state["editando_material_id"] = int(row["id"])
                st.rerun()
        else:
            cols[5].write("-")
        # Solo admin puede eliminar
        if permisos == "admin":
            if cols[6].button("🗑️", key=f"del_material_{row['id']}"):
                conn = get_connection()
                cur = conn.cursor()
                # Chequea FK: ¿está en materiales_proyecto?
                cur.execute("SELECT COUNT(*) FROM materiales_proyecto WHERE material_id=%s", (int(row["id"]),))
                cuenta = cur.fetchone()[0]
                if cuenta > 0:
                    st.error("No puedes eliminar este material porque está asociado a uno o más proyectos.")
                else:
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="materiales",
                        tipo_accion="eliminar",
                        descripcion=f"Eliminó material '{row['nombre']}' con id={row['id']}"
                    )
                    cur.execute("DELETE FROM materiales WHERE id=%s", (int(row["id"]),))
                    conn.commit()
                    st.success(f"Material {row['nombre']} eliminado.")
                    st.rerun()
                cur.close()
                conn.close()
        else:
            cols[6].write("-")

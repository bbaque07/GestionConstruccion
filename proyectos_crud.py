#proyects_crud.py
import streamlit as st
import pandas as pd
from config import get_connection
from bitacora import registrar_bitacora   # Registro de acciones en la bitácora

def crud_proyectos(permisos="admin"):
    st.title("CRUD de Proyectos")
    st.markdown("---")

    # --- Control de acceso ---
    if permisos == "invitado":
        st.warning("No tienes permisos para acceder a esta pantalla.")
        return

    # --- Estado de edición ---
    if "editando_proyecto_id" not in st.session_state:
        st.session_state["editando_proyecto_id"] = None

    # --- Edición de proyectos ---
    if st.session_state["editando_proyecto_id"]:
        conn = get_connection()
        df = pd.read_sql(
            "SELECT * FROM proyectos WHERE id=%s",
            conn,
            params=(st.session_state["editando_proyecto_id"],)
        )
        conn.close()
        if not df.empty:
            row = df.iloc[0]
            nombre = st.text_input("Nombre", value=row["nombre"], key="proyecto_nombre_edit")
            descripcion = st.text_area("Descripción", value=row["descripcion"], key="proyecto_desc_edit")
            fecha_inicio = st.date_input("Fecha de inicio", value=row["fecha_inicio"], key="proyecto_ini_edit")
            fecha_fin = st.date_input("Fecha de fin", value=row["fecha_fin"], key="proyecto_fin_edit")
            cliente_id = st.number_input("ID Cliente", min_value=1, value=row["cliente_id"] or 1, key="proyecto_cliente_edit")
            if permisos in ("admin", "usuario"):
                if st.button("Actualizar"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE proyectos SET nombre=%s, descripcion=%s, fecha_inicio=%s, fecha_fin=%s, cliente_id=%s WHERE id=%s",
                        (nombre, descripcion, fecha_inicio, fecha_fin, cliente_id, st.session_state["editando_proyecto_id"])
                    )
                    conn.commit()
                    # Registro en bitácora
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="proyectos",
                        tipo_accion="actualizar",
                        descripcion=f"Actualizó proyecto id={st.session_state['editando_proyecto_id']}: nombre={nombre}, descripcion={descripcion}, fechas={fecha_inicio} a {fecha_fin}, cliente_id={cliente_id}"
                    )
                    cur.close()
                    conn.close()
                    st.success("Proyecto actualizado.")
                    st.session_state["editando_proyecto_id"] = None
                    st.rerun()
            if st.button("Cancelar edición"):
                st.session_state["editando_proyecto_id"] = None
                st.rerun()

    # --- Creación de nuevo proyecto ---
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
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin, cliente_id) VALUES (%s, %s, %s, %s, %s)",
                            (nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)
                        )
                        conn.commit()
                        # Registro en bitácora
                        registrar_bitacora(
                            usuario=st.session_state["usuario"]["usuario"],
                            tabla="proyectos",
                            tipo_accion="crear",
                            descripcion=f"Creó proyecto '{nombre}' (descripcion={descripcion}, fechas={fecha_inicio} a {fecha_fin}, cliente_id={cliente_id})"
                        )
                        cur.close()
                        conn.close()
                        st.success("Proyecto registrado correctamente.")
                        st.rerun()
                    else:
                        st.error("El nombre es obligatorio.")

    # --- Tabla de proyectos ---
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM proyectos ORDER BY id", conn)
    conn.close()
    st.write("Listado de proyectos:")
    for idx, row in df.iterrows():
        cols = st.columns([1, 2, 2, 2, 2, 2, 1, 1])
        cols[0].write(row["id"])
        cols[1].write(row["nombre"])
        cols[2].write(row["descripcion"])
        cols[3].write(row["fecha_inicio"])
        cols[4].write(row["fecha_fin"])
        cols[5].write(row["cliente_id"])
        # Editar
        if permisos in ("admin", "usuario"):
            if cols[6].button("✏️", key=f"edit_proyecto_{row['id']}"):
                st.session_state["editando_proyecto_id"] = int(row["id"])
                st.rerun()
        else:
            cols[6].write("-")
        # Eliminar solo admin y validación de FK
        if permisos == "admin":
            if cols[7].button("🗑️", key=f"del_proyecto_{row['id']}"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM materiales_proyecto WHERE proyecto_id=%s", (int(row["id"]),))
                cuenta = cur.fetchone()[0]
                if cuenta > 0:
                    st.error("No puedes eliminar este proyecto porque está asociado a uno o más materiales de proyectos.")
                else:
                    registrar_bitacora(
                        usuario=st.session_state["usuario"]["usuario"],
                        tabla="proyectos",
                        tipo_accion="eliminar",
                        descripcion=f"Eliminó proyecto '{row['nombre']}' con id={row['id']}"
                    )
                    cur.execute("DELETE FROM proyectos WHERE id=%s", (int(row["id"]),))
                    conn.commit()
                    st.success(f"Proyecto {row['nombre']} eliminado.")
                    st.rerun()
                cur.close()
                conn.close()
        else:
            cols[7].write("-")
# Fin de la función crud_proyectos
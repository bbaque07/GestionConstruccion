# paginador.py
import streamlit as st
import pandas as pd
from config import get_connection

# --- Paginador para proveedores ---
def paginar_proveedores():
    st.title("🔍 Buscador de Proveedores")
    # Ciudades para filtro
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT ciudad FROM proveedores WHERE ciudad IS NOT NULL")
    ciudades = ["Todas"] + sorted([row[0] for row in cur.fetchall()])
    cur.close()
    conn.close()

    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o contacto:")
        ciudad = st.selectbox("Ciudad:", ciudades)

    condiciones = []
    params = []
    if busqueda:
        condiciones.append("(LOWER(nombre) LIKE %s OR LOWER(contacto) LIKE %s)")
        like = f"%{busqueda.lower()}%"
        params += [like, like]
    if ciudad != "Todas":
        condiciones.append("ciudad = %s")
        params.append(ciudad)
    where_sql = "WHERE " + " AND ".join(condiciones) if condiciones else ""

    items_por_pagina = 3
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM proveedores {where_sql}", params)
    total = cur.fetchone()[0]
    total_paginas = max(1, -(-total // items_por_pagina))
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="prov_page")
    offset = (pagina - 1) * items_por_pagina

    cur.execute(
        f"SELECT id, nombre, contacto, ciudad FROM proveedores {where_sql} ORDER BY id LIMIT %s OFFSET %s",
        params + [items_por_pagina, offset]
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    st.caption(f"Mostrando {len(rows)} de {total} resultados. Página {pagina} de {total_paginas}")

    if rows:
        df = pd.DataFrame(rows, columns=["id", "nombre", "contacto", "ciudad"])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No hay resultados con los filtros aplicados.")

# --- Paginador para clientes ---
def paginar_clientes():
    st.title("🔍 Buscador de Clientes")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT ciudad FROM clientes WHERE ciudad IS NOT NULL")
    ciudades = ["Todas"] + sorted([row[0] for row in cur.fetchall()])
    cur.close()
    conn.close()

    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o contacto:", key="cli_busq")
        ciudad = st.selectbox("Ciudad:", ciudades, key="cli_ciudad")

    condiciones = []
    params = []
    if busqueda:
        condiciones.append("(LOWER(nombre) LIKE %s OR LOWER(contacto) LIKE %s)")
        like = f"%{busqueda.lower()}%"
        params += [like, like]
    if ciudad != "Todas":
        condiciones.append("ciudad = %s")
        params.append(ciudad)
    where_sql = "WHERE " + " AND ".join(condiciones) if condiciones else ""

    items_por_pagina = 3
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM clientes {where_sql}", params)
    total = cur.fetchone()[0]
    total_paginas = max(1, -(-total // items_por_pagina))
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="cli_page")
    offset = (pagina - 1) * items_por_pagina

    cur.execute(
        f"SELECT id, nombre, contacto, ciudad FROM clientes {where_sql} ORDER BY id LIMIT %s OFFSET %s",
        params + [items_por_pagina, offset]
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    st.caption(f"Mostrando {len(rows)} de {total} resultados. Página {pagina} de {total_paginas}")

    if rows:
        df = pd.DataFrame(rows, columns=["id", "nombre", "contacto", "ciudad"])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No hay resultados con los filtros aplicados.")

# --- Paginador para materiales ---
def paginar_materiales():
    st.title("🔍 Buscador de Materiales")
    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o unidad:", key="mat_busq")

    condiciones = []
    params = []
    if busqueda:
        condiciones.append("(LOWER(nombre) LIKE %s OR LOWER(unidad) LIKE %s)")
        like = f"%{busqueda.lower()}%"
        params += [like, like]
    where_sql = "WHERE " + " AND ".join(condiciones) if condiciones else ""

    items_por_pagina = 3
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM materiales {where_sql}", params)
    total = cur.fetchone()[0]
    total_paginas = max(1, -(-total // items_por_pagina))
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="mat_page")
    offset = (pagina - 1) * items_por_pagina

    cur.execute(
        f"SELECT id, nombre, unidad, stock, precio FROM materiales {where_sql} ORDER BY id LIMIT %s OFFSET %s",
        params + [items_por_pagina, offset]
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    st.caption(f"Mostrando {len(rows)} de {total} resultados. Página {pagina} de {total_paginas}")

    if rows:
        df = pd.DataFrame(rows, columns=["id", "nombre", "unidad", "stock", "precio"])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No hay resultados con los filtros aplicados.")

# --- Paginador para proyectos ---
def paginar_proyectos():
    st.title("🔍 Buscador de Proyectos")
    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o descripción:", key="proy_busq")

    condiciones = []
    params = []
    if busqueda:
        condiciones.append("(LOWER(nombre) LIKE %s OR LOWER(descripcion) LIKE %s)")
        like = f"%{busqueda.lower()}%"
        params += [like, like]
    where_sql = "WHERE " + " AND ".join(condiciones) if condiciones else ""

    items_por_pagina = 3
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM proyectos {where_sql}", params)
    total = cur.fetchone()[0]
    total_paginas = max(1, -(-total // items_por_pagina))
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="proy_page")
    offset = (pagina - 1) * items_por_pagina

    cur.execute(
        f"SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, cliente_id FROM proyectos {where_sql} ORDER BY id LIMIT %s OFFSET %s",
        params + [items_por_pagina, offset]
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    st.caption(f"Mostrando {len(rows)} de {total} resultados. Página {pagina} de {total_paginas}")

    if rows:
        df = pd.DataFrame(rows, columns=["id", "nombre", "descripcion", "fecha_inicio", "fecha_fin", "cliente_id"])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No hay resultados con los filtros aplicados.")

# --- Fin de paginador.py ---

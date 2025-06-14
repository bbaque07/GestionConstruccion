#paginador.py
import streamlit as st
import pandas as pd
from math import ceil
from config import get_connection

# --- Paginador para proveedores ---
def paginar_proveedores():
    st.title("🔍 Buscador de Proveedores")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM proveedores ORDER BY id", conn)
    conn.close()
    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o contacto:")
        ciudades = ["Todas"] + sorted(df["ciudad"].dropna().unique())
        ciudad = st.selectbox("Ciudad:", ciudades)
    proveedores_filtrados = df.copy()
    if busqueda:
        proveedores_filtrados = proveedores_filtrados[
            proveedores_filtrados["nombre"].str.lower().str.contains(busqueda.lower()) |
            proveedores_filtrados["contacto"].str.lower().str.contains(busqueda.lower())
        ]
    if ciudad != "Todas":
        proveedores_filtrados = proveedores_filtrados[proveedores_filtrados["ciudad"] == ciudad]
    items_por_pagina = 3
    total_paginas = ceil(len(proveedores_filtrados) / items_por_pagina) if len(proveedores_filtrados) > 0 else 1
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="prov_page")
    inicio = (pagina - 1) * items_por_pagina
    fin = inicio + items_por_pagina
    datos_pagina = proveedores_filtrados.iloc[inicio:fin]
    st.caption(f"Mostrando {len(datos_pagina)} de {len(proveedores_filtrados)} resultados. Página {pagina} de {total_paginas}")
    if not datos_pagina.empty:
        st.dataframe(
            datos_pagina[["id", "nombre", "contacto", "ciudad"]],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.warning("No hay resultados con los filtros aplicados.")

# --- Paginador para clientes ---
def paginar_clientes():
    st.title("🔍 Buscador de Clientes")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM clientes ORDER BY id", conn)
    conn.close()
    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o contacto:", key="cli_busq")
        ciudades = ["Todas"] + sorted(df["ciudad"].dropna().unique())
        ciudad = st.selectbox("Ciudad:", ciudades, key="cli_ciudad")
    clientes_filtrados = df.copy()
    if busqueda:
        clientes_filtrados = clientes_filtrados[
            clientes_filtrados["nombre"].str.lower().str.contains(busqueda.lower()) |
            clientes_filtrados["contacto"].str.lower().str.contains(busqueda.lower())
        ]
    if ciudad != "Todas":
        clientes_filtrados = clientes_filtrados[clientes_filtrados["ciudad"] == ciudad]
    items_por_pagina = 3
    total_paginas = ceil(len(clientes_filtrados) / items_por_pagina) if len(clientes_filtrados) > 0 else 1
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="cli_page")
    inicio = (pagina - 1) * items_por_pagina
    fin = inicio + items_por_pagina
    datos_pagina = clientes_filtrados.iloc[inicio:fin]
    st.caption(f"Mostrando {len(datos_pagina)} de {len(clientes_filtrados)} resultados. Página {pagina} de {total_paginas}")
    if not datos_pagina.empty:
        st.dataframe(
            datos_pagina[["id", "nombre", "contacto", "ciudad"]],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.warning("No hay resultados con los filtros aplicados.")

# --- Paginador para materiales ---
def paginar_materiales():
    st.title("🔍 Buscador de Materiales")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM materiales ORDER BY id", conn)
    conn.close()
    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o unidad:", key="mat_busq")
    materiales_filtrados = df.copy()
    if busqueda:
        materiales_filtrados = materiales_filtrados[
            materiales_filtrados["nombre"].str.lower().str.contains(busqueda.lower()) |
            materiales_filtrados["unidad"].str.lower().str.contains(busqueda.lower())
        ]
    items_por_pagina = 3
    total_paginas = ceil(len(materiales_filtrados) / items_por_pagina) if len(materiales_filtrados) > 0 else 1
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="mat_page")
    inicio = (pagina - 1) * items_por_pagina
    fin = inicio + items_por_pagina
    datos_pagina = materiales_filtrados.iloc[inicio:fin]
    st.caption(f"Mostrando {len(datos_pagina)} de {len(materiales_filtrados)} resultados. Página {pagina} de {total_paginas}")
    if not datos_pagina.empty:
        st.dataframe(
            datos_pagina[["id", "nombre", "unidad", "stock", "precio"]],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.warning("No hay resultados con los filtros aplicados.")

# --- Paginador para proyectos ---
def paginar_proyectos():
    st.title("🔍 Buscador de Proyectos")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM proyectos ORDER BY id", conn)
    conn.close()
    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar por nombre o descripción:", key="proy_busq")
    proyectos_filtrados = df.copy()
    if busqueda:
        proyectos_filtrados = proyectos_filtrados[
            proyectos_filtrados["nombre"].str.lower().str.contains(busqueda.lower()) |
            proyectos_filtrados["descripcion"].str.lower().str.contains(busqueda.lower())
        ]
    items_por_pagina = 3
    total_paginas = ceil(len(proyectos_filtrados) / items_por_pagina) if len(proyectos_filtrados) > 0 else 1
    pagina = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, key="proy_page")
    inicio = (pagina - 1) * items_por_pagina
    fin = inicio + items_por_pagina
    datos_pagina = proyectos_filtrados.iloc[inicio:fin]
    st.caption(f"Mostrando {len(datos_pagina)} de {len(proyectos_filtrados)} resultados. Página {pagina} de {total_paginas}")
    if not datos_pagina.empty:
        st.dataframe(
            datos_pagina[["id", "nombre", "descripcion", "fecha_inicio", "fecha_fin", "cliente_id"]],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.warning("No hay resultados con los filtros aplicados.")

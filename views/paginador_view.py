import streamlit as st
from controllers.paginador_controller import get_ciudades, buscar_con_paginacion

def mostrar_paginador(tabla, titulo, campos, tipo_filtro, claves_ui):
    st.title(f"🔍 Buscador de {titulo}")

    ciudad = None
    with st.expander("🔍 Filtros", expanded=True):
        busqueda = st.text_input("Buscar:", key=claves_ui["busqueda"])

        if "ciudad" in claves_ui:
            ciudades = get_ciudades(tabla)
            ciudad = st.selectbox("Ciudad:", ciudades, key=claves_ui["ciudad"])

    pagina = st.number_input("Página", min_value=1, value=1, key=claves_ui["pagina"])
    items_por_pagina = 3

    df, total, total_paginas = buscar_con_paginacion(
        tabla=tabla,
        campos=campos,
        tipo_filtro=tipo_filtro,
        busqueda=busqueda,
        ciudad=ciudad,
        pagina=pagina,
        items_por_pagina=items_por_pagina
    )

    st.caption(f"Mostrando {len(df)} de {total} resultados. Página {pagina} de {total_paginas}")
    if not df.empty:
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No hay resultados con los filtros aplicados.")

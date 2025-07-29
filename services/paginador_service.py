import pandas as pd
from repositories.paginador_repository import contar_registros, obtener_resultados

def construir_filtros(busqueda, ciudad, tipo_filtro):
    condiciones = []
    params = []

    if busqueda:
        like = f"%{busqueda.lower()}%"
        if tipo_filtro == "nombre_contacto":
            condiciones.append("(LOWER(nombre) LIKE %s OR LOWER(contacto) LIKE %s)")
            params += [like, like]
        elif tipo_filtro == "nombre_unidad":
            condiciones.append("(LOWER(nombre) LIKE %s OR LOWER(unidad) LIKE %s)")
            params += [like, like]
        elif tipo_filtro == "nombre_descripcion":
            condiciones.append("(LOWER(nombre) LIKE %s OR LOWER(descripcion) LIKE %s)")
            params += [like, like]

    if ciudad and ciudad != "Todas":
        condiciones.append("ciudad = %s")
        params.append(ciudad)

    where_sql = "WHERE " + " AND ".join(condiciones) if condiciones else ""
    return where_sql, params

def paginar(tabla, campos, busqueda, ciudad, tipo_filtro, pagina, items_por_pagina):
    where_sql, params = construir_filtros(busqueda, ciudad, tipo_filtro)
    total = contar_registros(tabla, where_sql, params)
    total_paginas = max(1, -(-total // items_por_pagina))
    offset = (pagina - 1) * items_por_pagina

    rows = obtener_resultados(tabla, campos, where_sql, params, items_por_pagina, offset)
    df = pd.DataFrame(rows, columns=campos)

    return df, total, total_paginas 
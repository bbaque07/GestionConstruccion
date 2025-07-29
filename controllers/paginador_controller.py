from services.paginador_service import paginar
from repositories.paginador_repository import obtener_ciudades_distintas

def get_ciudades(tabla):
    return ["Todas"] + sorted(obtener_ciudades_distintas(tabla))

def buscar_con_paginacion(tabla, campos, tipo_filtro, busqueda, ciudad, pagina, items_por_pagina):
    return paginar(tabla, campos, busqueda, ciudad, tipo_filtro, pagina, items_por_pagina)

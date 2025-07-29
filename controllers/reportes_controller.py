from services.reportes_service import generar_reporte_consumo_materiales, generar_reporte_proveedores_proyectos

def obtener_consumo_materiales():
    return generar_reporte_consumo_materiales()

def obtener_proveedores_proyectos():
    return generar_reporte_proveedores_proyectos()

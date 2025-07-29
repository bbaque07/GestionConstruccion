import pandas as pd
from repositories.reportes_repository import get_consumo_materiales_por_proyecto, get_proveedores_proyectos

def generar_reporte_consumo_materiales():
    df = get_consumo_materiales_por_proyecto()
    if df.empty:
        return df, pd.DataFrame()
    total_por_proyecto = (
        df.groupby("proyecto")["costo_total"]
        .sum().reset_index()
        .rename(columns={"costo_total": "Total Proyecto"})
    )
    return df, total_por_proyecto

def generar_reporte_proveedores_proyectos():
    df = get_proveedores_proyectos()
    if df.empty:
        return df, pd.DataFrame()
    resumen = (
        df.groupby(["proveedor", "proyecto"])
        .agg({"cantidad": "sum"}).reset_index()
    )
    return df, resumen

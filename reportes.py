#reportes.py
import streamlit as st
import pandas as pd
from config import get_connection

def reporte_consumo_materiales():
    """Reporte 1: Consumo detallado de materiales por proyecto y totales."""
    st.header("📊 Consumo de Materiales por Proyecto")
    conn = get_connection()
    query = """
    SELECT
        p.nombre AS proyecto,
        c.nombre AS cliente,
        mp.fecha,
        m.nombre AS material,
        mp.cantidad,
        m.unidad,
        mp.precio_unitario,
        (mp.cantidad * mp.precio_unitario) AS costo_total
    FROM materiales_proyecto mp
    JOIN proyectos p ON mp.proyecto_id = p.id
    JOIN clientes c ON p.cliente_id = c.id
    JOIN materiales m ON mp.material_id = m.id
    ORDER BY p.nombre, mp.fecha, m.nombre
    """
    df = pd.read_sql(query, conn)
    conn.close()
    if not df.empty:
        total_por_proyecto = (
            df.groupby("proyecto")["costo_total"].sum()
            .reset_index().rename(columns={"costo_total": "Total Proyecto"})
        )
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.subheader("Totales por Proyecto")
        st.dataframe(total_por_proyecto, hide_index=True, use_container_width=True)
    else:
        st.info("No existen consumos de materiales registrados aún.")

def reporte_proveedores_proyectos():
    """Reporte 2: Relación de proveedores con proyectos y totales por proveedor/proyecto."""
    st.header("📊 Proveedores y Proyectos Abastecidos")
    conn = get_connection()
    query = """
    SELECT
        pr.nombre AS proveedor,
        p.nombre AS proyecto,
        c.nombre AS cliente,
        m.nombre AS material,
        mp.cantidad,
        m.unidad,
        mp.fecha
    FROM materiales_proyecto mp
    JOIN proveedores pr ON mp.proveedor_id = pr.id
    JOIN proyectos p ON mp.proyecto_id = p.id
    JOIN clientes c ON p.cliente_id = c.id
    JOIN materiales m ON mp.material_id = m.id
    ORDER BY pr.nombre, p.nombre, mp.fecha
    """
    df = pd.read_sql(query, conn)
    conn.close()
    if not df.empty:
        st.dataframe(df, hide_index=True, use_container_width=True)
        resumen = (
            df.groupby(["proveedor", "proyecto"])
            .agg({"cantidad": "sum"}).reset_index()
        )
        st.subheader("Total materiales entregados por Proveedor y Proyecto")
        st.dataframe(resumen, hide_index=True, use_container_width=True)
    else:
        st.info("No existen entregas de materiales aún.")

def mostrar_reportes():
    """Interfaz de selección para reportes avanzados."""
    st.title("📊 Reportes Avanzados del Sistema")
    reporte = st.selectbox(
        "Seleccione un reporte",
        (
            "Consumo de Materiales por Proyecto",
            "Proveedores y Proyectos Abastecidos"
        )
    )
    if reporte == "Consumo de Materiales por Proyecto":
        reporte_consumo_materiales()
    elif reporte == "Proveedores y Proyectos Abastecidos":
        reporte_proveedores_proyectos()

import streamlit as st
from controllers.reportes_controller import obtener_consumo_materiales, obtener_proveedores_proyectos

def mostrar_reporte_consumo_materiales():
    st.header("📊 Consumo de Materiales por Proyecto")
    df, resumen = obtener_consumo_materiales()
    if df.empty:
        st.info("No existen consumos de materiales registrados aún.")
    else:
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.subheader("Totales por Proyecto")
        st.dataframe(resumen, hide_index=True, use_container_width=True)

def mostrar_reporte_proveedores_proyectos():
    st.header("📊 Proveedores y Proyectos Abastecidos")
    df, resumen = obtener_proveedores_proyectos()
    if df.empty:
        st.info("No existen entregas de materiales aún.")
    else:
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.subheader("Total materiales entregados por Proveedor y Proyecto")
        st.dataframe(resumen, hide_index=True, use_container_width=True)

def mostrar_reportes():
    st.title("📊 Reportes Avanzados del Sistema")
    reporte = st.selectbox(
        "Seleccione un reporte",
        (
            "Consumo de Materiales por Proyecto",
            "Proveedores y Proyectos Abastecidos"
        )
    )
    if reporte == "Consumo de Materiales por Proyecto":
        mostrar_reporte_consumo_materiales()
    elif reporte == "Proveedores y Proyectos Abastecidos":
        mostrar_reporte_proveedores_proyectos()

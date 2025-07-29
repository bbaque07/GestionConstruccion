import platform
import streamlit as st
from repositories.bitacora_repository import insertar_registro_bitacora

def obtener_info_usuario():
    try:
        ip = st.query_params.get('ip', ['Desconocido'])[0]
    except:
        ip = "Desconocido"
    try:
        maquina = platform.node()
    except:
        maquina = "Desconocido"
    navegador = st.session_state.get("navegador", "Desconocido")
    return ip, maquina, navegador

def registrar_bitacora(usuario, tabla, tipo_accion, descripcion, hora_ingreso=None, hora_salida=None):
    ip, maquina, navegador = obtener_info_usuario()
    insertar_registro_bitacora(
        usuario=usuario,
        hora_ingreso=hora_ingreso,
        hora_salida=hora_salida,
        navegador=navegador,
        ip=ip,
        maquina=maquina,
        tabla=tabla,
        tipo_accion=tipo_accion,
        descripcion=descripcion
    )

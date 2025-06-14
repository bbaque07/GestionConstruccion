#bitacora.py
import streamlit as st
import socket
import platform
from datetime import datetime
from config import get_connection

def get_user_info():
    """
    Obtiene información del usuario actual:
    - IP (limitado en web, mejor en local)
    - Nombre de la máquina
    - Navegador (desde sesión)
    """
    try:
        # La IP real no es fácil de obtener desde Streamlit web, pero puedes intentar capturarla así:
        ip = st.experimental_get_query_params().get('ip', ['Desconocido'])[0]
    except:
        ip = "Desconocido"
    try:
        maquina = platform.node()  # Nombre del host local
    except:
        maquina = "Desconocido"
    navegador = st.session_state.get("navegador", "Desconocido")  # Guardado en login
    return ip, maquina, navegador

def registrar_bitacora(usuario, tabla, tipo_accion, descripcion, hora_ingreso=None, hora_salida=None):
    """
    Registra una acción en la tabla bitácora.
    Params:
        usuario: nombre de usuario que realiza la acción
        tabla: tabla afectada
        tipo_accion: tipo de acción ('crear', 'actualizar', 'eliminar', 'login', 'logout')
        descripcion: detalle de la acción realizada
        hora_ingreso: timestamp de ingreso (opcional)
        hora_salida: timestamp de salida (opcional)
    """
    ip, maquina, navegador = get_user_info()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bitacora (usuario, hora_ingreso, hora_salida, navegador, ip, maquina, tabla_afectada, tipo_accion, descripcion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            usuario,
            hora_ingreso,
            hora_salida,
            navegador,
            ip,
            maquina,
            tabla,
            tipo_accion,
            descripcion
        )
    )
    conn.commit()
    cur.close()
    conn.close()

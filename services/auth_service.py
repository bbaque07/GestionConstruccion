from repositories.auth_repository import (
    obtener_usuario_por_credenciales, existe_usuario_en_db,
    insertar_usuario
)
from services.bitacora_service import registrar_bitacora
from datetime import datetime
import streamlit as st

def autenticar_usuario(usuario, password):
    return obtener_usuario_por_credenciales(usuario, password)

def verificar_existencia_usuario(usuario):
    return existe_usuario_en_db(usuario)

def registrar_nuevo_usuario(nombre, usuario, password, rol):
    insertar_usuario(nombre, usuario, password, rol)
    registrar_bitacora(
        usuario=st.session_state["usuario"]["usuario"],
        tabla="usuarios",
        tipo_accion="crear",
        descripcion=f"Registró el usuario '{usuario}' con rol '{rol}'"
    )

def registrar_bitacora_login(usuario, navegador):
    registrar_bitacora(
        usuario=usuario,
        tabla="usuarios",
        tipo_accion="login",
        descripcion=f"Inicio de sesión (navegador: {navegador})",
        hora_ingreso=datetime.now()
    )

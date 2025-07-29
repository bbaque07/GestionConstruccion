from services.auth_service import (
    autenticar_usuario, verificar_existencia_usuario,
    registrar_nuevo_usuario, registrar_bitacora_login
)
import streamlit as st

def login_usuario(usuario, password, navegador):
    user = autenticar_usuario(usuario, password)
    if user:
        st.session_state["autenticado"] = True
        st.session_state["usuario"] = user
        st.session_state["navegador"] = navegador or "Desconocido"
        hora_ingreso = st.session_state["hora_ingreso"] = st.session_state.get("hora_ingreso") or st.session_state.get("hora_login") or None
        registrar_bitacora_login(user["usuario"], st.session_state["navegador"])
        return {"exito": True, "nombre": user["nombre"], "rol": user["rol"]}
    return {"exito": False}

def usuario_ya_existe(usuario):
    return verificar_existencia_usuario(usuario)

def registrar_usuario(nombre, usuario, password, rol):
    registrar_nuevo_usuario(nombre, usuario, password, rol)

def usuario_autenticado():
    return st.session_state.get("autenticado", False)

def es_admin():
    return st.session_state.get("usuario", {}).get("rol") == "admin"

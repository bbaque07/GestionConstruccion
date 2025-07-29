import streamlit as st
from controllers.auth_controller import login_usuario, registrar_usuario, usuario_ya_existe, usuario_autenticado, es_admin
from datetime import datetime

def mostrar_login():
    st.title("🔐 Inicio de sesión")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    navegador = st.text_input("¿Desde qué navegador accedes?", value="", help="Chrome, Firefox, Edge...")

    if st.button("Ingresar"):
        resultado = login_usuario(usuario, password, navegador)
        if resultado["exito"]:
            st.success(f"Bienvenido, {resultado['nombre']} ({resultado['rol']})")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

def mostrar_registro():
    st.title("📝 Registro de usuario (solo admin)")

    if not es_admin():
        st.warning("Solo el administrador puede registrar usuarios.")
        return

    nombre = st.text_input("Nombre completo")
    usuario = st.text_input("Usuario (login)")
    password = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["admin", "usuario", "invitado"])

    if st.button("Registrar"):
        if not nombre or not usuario or not password:
            st.error("Todos los campos son obligatorios.")
        elif usuario_ya_existe(usuario):
            st.error("El usuario ya existe.")
        else:
            registrar_usuario(nombre, usuario, password, rol)
            st.success(f"Usuario '{usuario}' creado correctamente.")
            st.session_state["mostrar_registro"] = False
            st.rerun()

    if st.button("Volver al login"):
        st.session_state["mostrar_registro"] = False
        st.rerun()

# auth.py
import streamlit as st
import pandas as pd
from config import get_connection
from datetime import datetime
from bitacora import registrar_bitacora

def autenticar(usuario, password):
    conn = get_connection()
    query = "SELECT id, nombre, usuario, rol FROM usuarios WHERE usuario=%s AND password=%s"
    df = pd.read_sql(query, conn, params=(usuario, password))
    conn.close()
    if not df.empty:
        return df.iloc[0].to_dict()
    return None

def existe_usuario(usuario):
    conn = get_connection()
    query = "SELECT id FROM usuarios WHERE usuario=%s"
    df = pd.read_sql(query, conn, params=(usuario,))
    conn.close()
    return not df.empty

def mostrar_login():
    st.title("🔐 Inicio de sesión")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    navegador = st.text_input("¿Desde qué navegador accedes? (opcional)", value="", help="Chrome, Firefox, Edge...")

    if st.button("Ingresar"):
        user = autenticar(usuario, password)
        if user:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = user
            st.session_state["navegador"] = navegador if navegador else "Desconocido"
            hora_ingreso = datetime.now()
            st.session_state["hora_ingreso"] = hora_ingreso
            registrar_bitacora(
                usuario=user["usuario"],
                tabla="usuarios",
                tipo_accion="login",
                descripcion=f"Inicio de sesión (navegador: {st.session_state['navegador']})",
                hora_ingreso=hora_ingreso
            )
            st.success(f"Bienvenido, {user['nombre']} ({user['rol']})")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
    
def mostrar_registro():
    st.title("📝 Registro de usuario (solo admin)")
    if st.session_state.get("usuario", {}).get("rol") != "admin":
        st.warning("Solo el administrador puede registrar usuarios.")
        return
    nombre = st.text_input("Nombre completo")
    usuario = st.text_input("Usuario (login)")
    password = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["admin", "usuario", "invitado"])
    if st.button("Registrar"):
        if not nombre or not usuario or not password:
            st.error("Todos los campos son obligatorios.")
        elif existe_usuario(usuario):
            st.error("El usuario ya existe.")
        else:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, usuario, password, rol) VALUES (%s, %s, %s, %s)",
                (nombre, usuario, password, rol)
            )
            conn.commit()
            cur.close()
            conn.close()
            registrar_bitacora(
                usuario=st.session_state["usuario"]["usuario"],
                tabla="usuarios",
                tipo_accion="crear",
                descripcion=f"Registró el usuario '{usuario}' con rol '{rol}'"
            )
            st.success(f"Usuario '{usuario}' creado correctamente.")
            st.session_state["mostrar_registro"] = False
            st.rerun()
    if st.button("Volver al login"):
        st.session_state["mostrar_registro"] = False
        st.rerun()

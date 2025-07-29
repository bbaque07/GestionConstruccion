#app.py
import streamlit as st
from views.proveedores_views import crud_proveedores
from views.clientes_view import mostrar_clientes
from controllers.materiales_controller import crud_materiales
from views.proyectos_view import vista_crud_proyectos
from views.paginador_view import mostrar_paginador
from views.reportes_view import mostrar_reportes
from views.auth_view import mostrar_login, mostrar_registro
from services.bitacora_service import registrar_bitacora
from datetime import datetime

# --- Presentación: Pantalla principal y menú lateral ---
def logout():
    """Cierra la sesión del usuario, registra la acción en la bitácora y limpia el estado."""
    hora_salida = datetime.now()
    if "usuario" in st.session_state:
        registrar_bitacora(
            usuario=st.session_state["usuario"]["usuario"],
            tabla="usuarios",
            tipo_accion="logout",
            descripcion="Cierre de sesión",
            hora_ingreso=st.session_state.get("hora_ingreso"),
            hora_salida=hora_salida
        )
    st.session_state.clear()
    st.success("Sesión cerrada.")
    st.rerun()

def main():
    """Controla el flujo principal de la app según el rol y autenticación del usuario."""

    # --- Estado inicial ---
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = {}

    # --- Login y Registro (solo presentación, lógica en auth.py) ---
    if not st.session_state["autenticado"]:
        if st.session_state.get("mostrar_registro"):
            mostrar_registro()
        else:
            mostrar_login()
        return

    # --- Asigna el rol del usuario autenticado ---
    rol = st.session_state["usuario"].get("rol", "invitado")

    # --- Menú lateral dinámico según rol ---
    st.sidebar.title(f"Menú ({rol.title()})")
    st.sidebar.write(f"Usuario: {st.session_state['usuario'].get('nombre')}")
    if st.sidebar.button("Cerrar sesión"):
        logout()

    # --- Definición de opciones de menú según rol (capa presentación) ---
    menu_admin = [
        "CRUD Proveedores", "CRUD Clientes", "CRUD Materiales", "CRUD Proyectos",
        "Paginador Proveedores", "Paginador Clientes", "Paginador Materiales", "Paginador Proyectos",
        "Reportes", "Registrar usuario"
    ]
    menu_usuario = [
        "CRUD Proveedores", "CRUD Clientes", "CRUD Materiales", "CRUD Proyectos",
        "Paginador Proveedores", "Paginador Clientes", "Paginador Materiales", "Paginador Proyectos",
        "Reportes"
    ]
    menu_invitado = [
        "Paginador Proveedores", "Paginador Clientes", "Paginador Materiales", "Paginador Proyectos"
    ]

    # --- Selección de menú (solo muestra las opciones habilitadas según rol) ---
    menu = menu_admin if rol == "admin" else menu_usuario if rol == "usuario" else menu_invitado
    pantalla = st.sidebar.selectbox("Selecciona una pantalla", menu)

    # --- Ruteo a cada pantalla/module ---
    if pantalla == "CRUD Proveedores":
        crud_proveedores(permisos=rol)
    elif pantalla == "CRUD Clientes":
        mostrar_clientes(permisos=rol)
    elif pantalla == "CRUD Materiales":
        crud_materiales(permisos=rol)
    elif pantalla == "CRUD Proyectos":
        vista_crud_proyectos(permisos=rol)
    elif pantalla == "Paginador Proveedores":
        mostrar_paginador("proveedores", "Proveedores", ["nombre", "contacto", "telefono"], "nombre_contacto", {
            "busqueda": "busq_prov", "ciudad": "ciudad_prov", "pagina": "pag_prov"
        })
    elif pantalla == "Paginador Clientes":
        mostrar_paginador("clientes", "Clientes", ["nombre", "contacto", "telefono"], "nombre_contacto", {
            "busqueda": "busq_cli", "ciudad": "ciudad_cli", "pagina": "pag_cli"
        })
    elif pantalla == "Paginador Materiales":
        mostrar_paginador("materiales", "Materiales", ["nombre", "unidad"], "nombre_unidad", {
            "busqueda": "busq_mat", "pagina": "pag_mat"
        })
    elif pantalla == "Paginador Proyectos":
        mostrar_paginador("proyectos", "Proyectos", ["nombre", "descripcion"], "nombre_descripcion", {
            "busqueda": "busq_proy", "pagina": "pag_proy"
        })
    elif pantalla == "Reportes":
        mostrar_reportes()
    elif pantalla == "Registrar usuario":
        mostrar_registro()

# --- Entry point (capa presentación) ---
if __name__ == "__main__":
    main()

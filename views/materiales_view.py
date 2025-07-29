import streamlit as st

def mostrar_materiales(materiales, permisos):
    st.write("Listado de materiales:")
    for row in materiales:
        cols = st.columns([1, 2, 2, 2, 2, 1, 1])
        cols[0].write(row["id"])
        cols[1].write(row["nombre"])
        cols[2].write(row["unidad"])
        cols[3].write(row["stock"])
        cols[4].write(row["precio"])
        if permisos in ("admin", "usuario"):
            if cols[5].button("✏️", key=f"edit_material_{row['id']}"):
                st.session_state["editando_material_id"] = row["id"]
                st.rerun()
        else:
            cols[5].write("-")
        if permisos == "admin":
            if cols[6].button("🗑️", key=f"del_material_{row['id']}"):
                st.session_state["eliminando_material_id"] = row["id"]
                st.rerun()
        else:
            cols[6].write("-")


def formulario_creacion_material(callback):
    with st.form("form_nuevo_material"):
        nombre = st.text_input("Nombre", key="material_nombre")
        unidad = st.text_input("Unidad", key="material_unidad")
        stock = st.number_input("Stock", min_value=0, key="material_stock")
        precio = st.number_input("Precio", min_value=0.0, key="material_precio")
        if st.form_submit_button("Guardar"):
            callback(nombre, unidad, stock, precio)


def formulario_edicion_material(material, callback_actualizar, callback_cancelar):
    nombre = st.text_input("Nombre", value=material["nombre"], key="material_nombre_edit")
    unidad = st.text_input("Unidad", value=material["unidad"], key="material_unidad_edit")
    stock = st.number_input("Stock", min_value=0, value=material["stock"], key="material_stock_edit")
    precio = st.number_input("Precio", min_value=0.0, value=float(material["precio"]), key="material_precio_edit")

    if st.button("Actualizar"):
        callback_actualizar(nombre, unidad, stock, precio)
    if st.button("Cancelar edición"):
        callback_cancelar()

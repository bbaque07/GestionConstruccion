from services.proyectos_service import (
    listar_proyectos, insertar_proyecto, editar_proyecto,
    borrar_proyecto, get_proyecto_por_id
)

def obtener_proyectos():
    return listar_proyectos()

def crear_proyecto(nombre, descripcion, fecha_inicio, fecha_fin, cliente_id):
    insertar_proyecto(nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)

def actualizar_proyecto(id, nombre, descripcion, fecha_inicio, fecha_fin, cliente_id):
    editar_proyecto(id, nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)

def eliminar_proyecto(id, nombre):
    return borrar_proyecto(id, nombre)

def obtener_proyecto_por_id(id):
    return get_proyecto_por_id(id)

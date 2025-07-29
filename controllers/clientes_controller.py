from services.clientes_service import crear_cliente_service, actualizar_cliente_service, eliminar_cliente_service
from repositories.clientes_repository import obtener_todos_los_clientes, obtener_cliente_por_id

def get_clientes():
    return obtener_todos_los_clientes()

def get_cliente_por_id(cliente_id):
    df = obtener_cliente_por_id(cliente_id)
    return df.iloc[0] if not df.empty else None

def crear_cliente(data):
    crear_cliente_service(**data)

def actualizar_cliente(cliente_id, data):
    actualizar_cliente_service(cliente_id, **data)

def eliminar_cliente(cliente_id, nombre):
    return eliminar_cliente_service(cliente_id, nombre)

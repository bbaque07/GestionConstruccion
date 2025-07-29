import pandas as pd
from config import get_connection

def obtener_todos_proyectos():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM proyectos ORDER BY id desc", conn)
    conn.close()
    return df

def crear_nuevo_proyecto(nombre, descripcion, fecha_inicio, fecha_fin, cliente_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin, cliente_id) VALUES (%s, %s, %s, %s, %s)",
        (nombre, descripcion, fecha_inicio, fecha_fin, cliente_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def actualizar_proyecto_db(id, nombre, descripcion, fecha_inicio, fecha_fin, cliente_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE proyectos SET nombre=%s, descripcion=%s, fecha_inicio=%s, fecha_fin=%s, cliente_id=%s WHERE id=%s",
        (nombre, descripcion, fecha_inicio, fecha_fin, cliente_id, id)
    )
    conn.commit()
    cur.close()
    conn.close()

def eliminar_proyecto_db(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM proyectos WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()

def proyecto_en_uso(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM materiales_proyecto WHERE proyecto_id=%s", (id,))
    cuenta = cur.fetchone()[0]
    cur.close()
    conn.close()
    return cuenta > 0

def buscar_proyecto_por_id(id):
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM proyectos WHERE id=%s", conn, params=(id,))
    conn.close()
    return df.iloc[0].to_dict() if not df.empty else None

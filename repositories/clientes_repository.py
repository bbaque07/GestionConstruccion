import pandas as pd
from config import get_connection

# ────────────── CRUD ─────────────────

def obtener_cliente_por_id(cliente_id):
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM clientes WHERE id=%s", conn, params=(cliente_id,))
    conn.close()
    return df

def obtener_todos_los_clientes():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM clientes ORDER BY id DESC", conn)
    conn.close()
    return df

def crear_cliente(nombre, contacto, telefono, direccion, ciudad, ruc):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clientes (nombre, contacto, telefono, direccion, ciudad, ruc)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, contacto, telefono, direccion, ciudad, ruc))
    conn.commit()
    cur.close()
    conn.close()

def actualizar_cliente(cliente_id, nombre, contacto, telefono, direccion, ciudad, ruc):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE clientes
        SET nombre=%s, contacto=%s, telefono=%s, direccion=%s, ciudad=%s, ruc=%s
        WHERE id=%s
    """, (nombre, contacto, telefono, direccion, ciudad, ruc, cliente_id))
    conn.commit()
    cur.close()
    conn.close()

def eliminar_cliente(cliente_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
    conn.commit()
    cur.close()
    conn.close()

def cliente_esta_en_proyectos(cliente_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM proyectos WHERE cliente_id=%s", (cliente_id,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count > 0

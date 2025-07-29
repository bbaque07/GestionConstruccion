# repositories/proveedor_repository.py
from config import get_connection

def insertar_proveedor(nombre, contacto, telefono, direccion, ciudad, ruc):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO proveedores (nombre, contacto, telefono, direccion, ciudad, ruc)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, contacto, telefono, direccion, ciudad, ruc))
    conn.commit()
    cur.close()
    conn.close()

def obtener_todos_proveedores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM proveedores ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(id=r[0], nombre=r[1], contacto=r[2], telefono=r[3], direccion=r[4], ciudad=r[5], ruc=r[6]) for r in rows]

def obtener_proveedor_db(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    if r:
        return dict(id=r[0], nombre=r[1], contacto=r[2], telefono=r[3], direccion=r[4], ciudad=r[5], ruc=r[6])
    return None

def actualizar_proveedor_db(id, nombre, contacto, telefono, direccion, ciudad, ruc):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE proveedores SET nombre=%s, contacto=%s, telefono=%s,
        direccion=%s, ciudad=%s, ruc=%s WHERE id=%s
    """, (nombre, contacto, telefono, direccion, ciudad, ruc, id))
    conn.commit()
    cur.close()
    conn.close()

def eliminar_proveedor_db(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM proveedores WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()

def proveedor_tiene_materiales(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM materiales_proyecto WHERE proveedor_id=%s", (id,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count > 0

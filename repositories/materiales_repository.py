from config import get_connection

def insertar_material(nombre, unidad, stock, precio):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO materiales (nombre, unidad, stock, precio) VALUES (%s, %s, %s, %s)",
        (nombre, unidad, stock, precio)
    )
    conn.commit()
    cur.close()
    conn.close()


def obtener_todos_los_materiales():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM materiales ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(cols, row)) for row in rows]


def obtener_material_por_id_db(id_):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM materiales WHERE id = %s", (id_,))
    row = cur.fetchone()
    cols = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return dict(zip(cols, row)) if row else None


def actualizar_material_db(id_, nombre, unidad, stock, precio):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE materiales SET nombre=%s, unidad=%s, stock=%s, precio=%s WHERE id=%s",
        (nombre, unidad, stock, precio, id_)
    )
    conn.commit()
    cur.close()
    conn.close()


def verificar_relacion_material(id_):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM materiales_proyecto WHERE material_id = %s", (id_,))
    cuenta = cur.fetchone()[0]
    cur.close()
    conn.close()
    return cuenta > 0


def eliminar_material_db(id_):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM materiales WHERE id = %s", (id_,))
    conn.commit()
    cur.close()
    conn.close()

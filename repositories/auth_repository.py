import pandas as pd
from config import get_connection

def obtener_usuario_por_credenciales(usuario, password):
    conn = get_connection()
    query = "SELECT id, nombre, usuario, rol FROM usuarios WHERE usuario=%s AND password=%s"
    df = pd.read_sql(query, conn, params=(usuario, password))
    conn.close()
    return df.iloc[0].to_dict() if not df.empty else None

def existe_usuario_en_db(usuario):
    conn = get_connection()
    query = "SELECT id FROM usuarios WHERE usuario=%s"
    df = pd.read_sql(query, conn, params=(usuario,))
    conn.close()
    return not df.empty

def insertar_usuario(nombre, usuario, password, rol):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuarios (nombre, usuario, password, rol) VALUES (%s, %s, %s, %s)",
        (nombre, usuario, password, rol)
    )
    conn.commit()
    cur.close()
    conn.close()

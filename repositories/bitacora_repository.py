# repositories/bitacora_repository.py
from config import get_connection

def insertar_registro_bitacora(usuario, hora_ingreso, hora_salida, navegador, ip, maquina, tabla, tipo_accion, descripcion):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bitacora (
            usuario, hora_ingreso, hora_salida, navegador,
            ip, maquina, tabla_afectada, tipo_accion, descripcion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        usuario, hora_ingreso, hora_salida, navegador,
        ip, maquina, tabla, tipo_accion, descripcion
    ))
    conn.commit()
    cur.close()
    conn.close()

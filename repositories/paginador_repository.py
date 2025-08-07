# repositories/paginador_repository.py
from config import get_connection

def obtener_ciudades_distintas(tabla):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT ciudad FROM {tabla} WHERE ciudad IS NOT NULL")
    ciudades = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return ciudades

def contar_registros(tabla, where_sql, params):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {tabla} {where_sql}", params)
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total

def obtener_resultados(tabla, campos, where_sql, params, limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT {', '.join(campos)} FROM {tabla} {where_sql} ORDER BY id LIMIT %s OFFSET %s",
        params + [limit, offset]
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

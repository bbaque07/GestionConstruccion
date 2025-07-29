import pandas as pd
from config import get_connection

def get_consumo_materiales_por_proyecto():
    query = """
    SELECT
        p.nombre AS proyecto,
        c.nombre AS cliente,
        mp.fecha,
        m.nombre AS material,
        mp.cantidad,
        m.unidad,
        mp.precio_unitario,
        (mp.cantidad * mp.precio_unitario) AS costo_total
    FROM materiales_proyecto mp
    JOIN proyectos p ON mp.proyecto_id = p.id
    JOIN clientes c ON p.cliente_id = c.id
    JOIN materiales m ON mp.material_id = m.id
    ORDER BY p.nombre, mp.fecha, m.nombre
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_proveedores_proyectos():
    query = """
    SELECT
        pr.nombre AS proveedor,
        p.nombre AS proyecto,
        c.nombre AS cliente,
        m.nombre AS material,
        mp.cantidad,
        m.unidad,
        mp.fecha
    FROM materiales_proyecto mp
    JOIN proveedores pr ON mp.proveedor_id = pr.id
    JOIN proyectos p ON mp.proyecto_id = p.id
    JOIN clientes c ON p.cliente_id = c.id
    JOIN materiales m ON mp.material_id = m.id
    ORDER BY pr.nombre, p.nombre, mp.fecha
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

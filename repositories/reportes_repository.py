# repositories/reportes_repository.py
import pandas as pd
from config import get_connection

def get_consumo_materiales_por_proyecto():
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM vista_consumo_materiales", conn)
        return df
    except Exception as e:
        print(f"Error en get_consumo_materiales_por_proyecto: {str(e)}")
        raise
    finally:
        conn.close()

def get_proveedores_proyectos():
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM vista_proveedores_proyectos", conn)
        return df
    except Exception as e:
        print(f"Error en get_proveedores_proyectos: {str(e)}")
        raise
    finally:
        conn.close()
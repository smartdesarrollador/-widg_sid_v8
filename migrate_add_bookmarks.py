"""
Migración: Agregar tabla de bookmarks para el navegador embebido
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    """Agrega la tabla de bookmarks si no existe."""
    db_path = "widget_sidebar.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='bookmarks'
        """)

        if cursor.fetchone():
            logger.info("La tabla 'bookmarks' ya existe. No se requiere migración.")
            return

        # Crear tabla de bookmarks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                folder TEXT DEFAULT NULL,
                icon TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                order_index INTEGER DEFAULT 0
            )
        """)

        # Crear índices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bookmarks_order ON bookmarks(order_index)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bookmarks_url ON bookmarks(url)
        """)

        conn.commit()
        logger.info("✓ Tabla 'bookmarks' creada exitosamente")
        logger.info("✓ Índices creados exitosamente")

    except Exception as e:
        logger.error(f"Error en la migración: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    logger.info("Iniciando migración para agregar tabla de bookmarks...")
    migrate()
    logger.info("Migración completada")

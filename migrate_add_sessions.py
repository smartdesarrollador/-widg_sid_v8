"""
Migración: Agregar tablas de sesiones para el navegador
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    """Agrega las tablas de sesiones para el navegador."""
    db_path = "widget_sidebar.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='browser_sessions'
        """)

        if cursor.fetchone():
            logger.info("La tabla 'browser_sessions' ya existe. No se requiere migración.")
            return

        # Crear tabla de sesiones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS browser_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                is_auto_save BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Crear tabla de pestañas de sesión
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_tabs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                title TEXT DEFAULT 'Nueva pestaña',
                position INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES browser_sessions(id) ON DELETE CASCADE
            )
        """)

        # Crear índices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_tabs_session_id ON session_tabs(session_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_tabs_position ON session_tabs(position)
        """)

        conn.commit()
        logger.info("✓ Tabla 'browser_sessions' creada exitosamente")
        logger.info("✓ Tabla 'session_tabs' creada exitosamente")
        logger.info("✓ Índices creados exitosamente")

    except Exception as e:
        logger.error(f"Error en la migración: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    logger.info("Iniciando migración para agregar tablas de sesiones...")
    migrate()
    logger.info("Migración completada")

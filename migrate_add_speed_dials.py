"""
Migración: Agregar tabla de speed_dials para el navegador embebido
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    """Agrega la tabla de speed_dials si no existe."""
    db_path = "widget_sidebar.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='speed_dials'
        """)

        if cursor.fetchone():
            logger.info("La tabla 'speed_dials' ya existe. No se requiere migración.")
            return

        # Crear tabla de speed_dials
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS speed_dials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                thumbnail_path TEXT DEFAULT NULL,
                background_color TEXT DEFAULT '#16213e',
                icon TEXT DEFAULT '🌐',
                position INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Crear índice
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_speed_dials_position ON speed_dials(position)
        """)

        # Agregar algunos speed dials por defecto
        default_speed_dials = [
            ("Google", "https://www.google.com", "🔍", "#4285f4"),
            ("YouTube", "https://www.youtube.com", "📺", "#ff0000"),
            ("GitHub", "https://www.github.com", "💻", "#24292e"),
        ]

        for i, (title, url, icon, color) in enumerate(default_speed_dials):
            cursor.execute("""
                INSERT INTO speed_dials (title, url, icon, background_color, position)
                VALUES (?, ?, ?, ?, ?)
            """, (title, url, icon, color, i))

        conn.commit()
        logger.info("✓ Tabla 'speed_dials' creada exitosamente")
        logger.info("✓ Índice creado exitosamente")
        logger.info(f"✓ {len(default_speed_dials)} speed dials por defecto agregados")

    except Exception as e:
        logger.error(f"Error en la migración: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    logger.info("Iniciando migración para agregar tabla de speed_dials...")
    migrate()
    logger.info("Migración completada")

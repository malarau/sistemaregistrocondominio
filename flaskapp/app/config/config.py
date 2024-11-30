from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

# Configuración de la base de datos
# SERÍA IDEAL UTILIZAR LAS MISMAS VARIABLES DE ENTORNO USADAS EN DOCKER-COMPOSE PARA DEFINIR LA DB 
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'pgdatabase'),
    'user': os.getenv('DB_USER', 'pguser'),
    'password': os.getenv('DB_PASSWORD', 'pgpassword')
}

# Crear URL de conexión
DATABASE_URL = (
    f"postgresql://{DATABASE_CONFIG['user']}:"
    f"{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:"
    f"{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

# Motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sesión de base de datos
db_session = scoped_session(SessionLocal)
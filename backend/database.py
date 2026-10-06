import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# =====================================================================
# CARGA DE CREDENCIALES
# Lee las variables de entorno definidas en el archivo oculto .env (como el usuario, contraseña y puerto de PostgreSQL)
# =====================================================================
load_dotenv()

# Obtenemos la URL de conexión a la base de datos desde el archivo .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# =====================================================================
# CONFIGURACIÓN DEL MOTOR Y SESIONES DE SQLALCHEMY
# =====================================================================

# Crea el "motor" (engine) principal que gestiona las conexiones físicas con PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fábrica de sesiones (SessionLocal): cada vez que una ruta necesite hablar con la BD, pedirá una sesión de aquí
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa: de aquí heredarán todos tus modelos (tablas) para que SQLAlchemy los reconozca
Base = declarative_base()

# =====================================================================
# GESTOR DE CONEXIÓN POR PETICIÓN (DEPENDENCY INJECTION)
# =====================================================================
def get_db():
    """
    Función de apoyo (Dependency) que se inyecta en cada ruta de FastAPI.
    Abre una conexión con la base de datos para la petición actual,
    y se asegura de cerrarla automáticamente al terminar (incluso si ocurre un error).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
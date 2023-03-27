from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a la base de datos
class DBSettings(BaseSettings):
    db_user: str = 'root'
    db_password: str = 'luisdavid2906'
    db_host: str = '127.0.0.1'
    db_port: int = '3306'
    db_name: str = 'credit_qa'

    class Config:
        env_prefix = "db_"

# Crear la URL de conexión
settings = DBSettings()
db_url = f"mysql+mysqlconnector://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# Crear un motor SQLAlchemy
engine = create_engine(db_url)

# Crear una clase base de declaraciones
Base = declarative_base()

# Crear una sesión de base de datos
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
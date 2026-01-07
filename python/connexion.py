"""
Module de connexion à la base de données PostgreSQL
Utilise SQLAlchemy avec sessionmaker
"""

import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Charger le .env depuis le dossier parent
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# Configuration de la base de données (depuis .env)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'gestion_stock')
DB_USER = os.getenv('POSTGRES_USER', 'stock_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'stock_password')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Créer la factory de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles ORM
Base = declarative_base()


def get_session():
    """
    Crée et retourne une nouvelle session.
    À utiliser avec un context manager ou à fermer manuellement.
    """
    return SessionLocal()


def test_connexion():
    """
    Teste la connexion à la base de données.
    Retourne True si OK, False sinon.
    """
    try:
        session = get_session()
        session.execute(text("SELECT 1"))
        session.close()
        return True
    except Exception as e:
        print(f"Erreur de test de connexion: {e}")
        return False


if __name__ == "__main__":
    # Test de la connexion
    if test_connexion():
        print("✓ Connexion à la base de données réussie!")
    else:
        print("✗ Échec de la connexion à la base de données.")

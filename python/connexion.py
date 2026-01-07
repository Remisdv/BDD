"""
Module de connexion à la base de données PostgreSQL
Utilise psycopg2 pour la connexion directe
"""

import psycopg2
import os
from pathlib import Path

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
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'gestion_stock'),
    'user': os.getenv('POSTGRES_USER', 'stock_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'stock_password')
}


def get_connexion():
    """
    Crée et retourne une connexion à la base de données.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        raise


def get_curseur(conn):
    """
    Crée et retourne un curseur à partir d'une connexion.
    """
    return conn.cursor()


def fermer_connexion(conn, curseur=None):
    """
    Ferme proprement le curseur et la connexion.
    """
    if curseur:
        curseur.close()
    if conn:
        conn.close()


def test_connexion():
    """
    Teste la connexion à la base de données.
    Retourne True si OK, False sinon.
    """
    try:
        conn = get_connexion()
        curseur = get_curseur(conn)
        curseur.execute("SELECT 1")
        fermer_connexion(conn, curseur)
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

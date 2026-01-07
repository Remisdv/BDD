"""
CRUD pour la table categories
"""

from connexion import get_connexion, get_curseur, fermer_connexion


def creer_categorie(nom, description=None):
    """Créer une nouvelle catégorie"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "INSERT INTO categories (nom, description) VALUES (%s, %s) RETURNING id",
            (nom, description)
        )
        categorie_id = curseur.fetchone()[0]
        conn.commit()
        return categorie_id
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        fermer_connexion(conn, curseur)


def lire_categories():
    """Lire toutes les catégories"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("SELECT id, nom, description FROM categories ORDER BY nom")
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def lire_categorie(categorie_id):
    """Lire une catégorie par son ID"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "SELECT id, nom, description FROM categories WHERE id = %s",
            (categorie_id,)
        )
        return curseur.fetchone()
    finally:
        fermer_connexion(conn, curseur)


def modifier_categorie(categorie_id, nom=None, description=None):
    """Modifier une catégorie existante"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        updates = []
        values = []
        
        if nom is not None:
            updates.append("nom = %s")
            values.append(nom)
        if description is not None:
            updates.append("description = %s")
            values.append(description)
        
        if not updates:
            return False
        
        values.append(categorie_id)
        query = f"UPDATE categories SET {', '.join(updates)} WHERE id = %s"
        curseur.execute(query, values)
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def supprimer_categorie(categorie_id):
    """Supprimer une catégorie"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("DELETE FROM categories WHERE id = %s", (categorie_id,))
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)

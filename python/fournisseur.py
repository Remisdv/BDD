"""
CRUD pour la table fournisseurs
"""

from connexion import get_connexion, get_curseur, fermer_connexion


def creer_fournisseur(nom, email=None, telephone=None, adresse=None):
    """Créer un nouveau fournisseur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            """INSERT INTO fournisseurs (nom, email, telephone, adresse) 
               VALUES (%s, %s, %s, %s) RETURNING id""",
            (nom, email, telephone, adresse)
        )
        fournisseur_id = curseur.fetchone()[0]
        conn.commit()
        return fournisseur_id
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        fermer_connexion(conn, curseur)


def lire_fournisseurs():
    """Lire tous les fournisseurs"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "SELECT id, nom, email, telephone, adresse FROM fournisseurs ORDER BY nom"
        )
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def lire_fournisseur(fournisseur_id):
    """Lire un fournisseur par son ID"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "SELECT id, nom, email, telephone, adresse FROM fournisseurs WHERE id = %s",
            (fournisseur_id,)
        )
        return curseur.fetchone()
    finally:
        fermer_connexion(conn, curseur)


def modifier_fournisseur(fournisseur_id, nom=None, email=None, telephone=None, adresse=None):
    """Modifier un fournisseur existant"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        updates = []
        values = []
        
        if nom is not None:
            updates.append("nom = %s")
            values.append(nom)
        if email is not None:
            updates.append("email = %s")
            values.append(email)
        if telephone is not None:
            updates.append("telephone = %s")
            values.append(telephone)
        if adresse is not None:
            updates.append("adresse = %s")
            values.append(adresse)
        
        if not updates:
            return False
        
        values.append(fournisseur_id)
        query = f"UPDATE fournisseurs SET {', '.join(updates)} WHERE id = %s"
        curseur.execute(query, values)
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def supprimer_fournisseur(fournisseur_id):
    """Supprimer un fournisseur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("DELETE FROM fournisseurs WHERE id = %s", (fournisseur_id,))
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)

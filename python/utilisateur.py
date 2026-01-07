"""
CRUD pour la table utilisateurs (sécurité)
"""

import hashlib
from connexion import get_connexion, get_curseur, fermer_connexion


def hasher_mot_de_passe(mot_de_passe):
    """Hasher un mot de passe avec SHA256"""
    return hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()


def creer_utilisateur(username, mot_de_passe, role='user'):
    """Créer un nouvel utilisateur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        password_hash = hasher_mot_de_passe(mot_de_passe)
        curseur.execute(
            """INSERT INTO utilisateurs (username, password_hash, role) 
               VALUES (%s, %s, %s) RETURNING id""",
            (username, password_hash, role)
        )
        utilisateur_id = curseur.fetchone()[0]
        conn.commit()
        return utilisateur_id
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        fermer_connexion(conn, curseur)


def authentifier(username, mot_de_passe):
    """Authentifier un utilisateur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        password_hash = hasher_mot_de_passe(mot_de_passe)
        curseur.execute(
            """SELECT id, username, role FROM utilisateurs 
               WHERE username = %s AND password_hash = %s AND actif = TRUE""",
            (username, password_hash)
        )
        return curseur.fetchone()
    finally:
        fermer_connexion(conn, curseur)


def lire_utilisateurs():
    """Lire tous les utilisateurs"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "SELECT id, username, role, actif FROM utilisateurs ORDER BY username"
        )
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def lire_utilisateur(utilisateur_id):
    """Lire un utilisateur par son ID"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "SELECT id, username, role, actif FROM utilisateurs WHERE id = %s",
            (utilisateur_id,)
        )
        return curseur.fetchone()
    finally:
        fermer_connexion(conn, curseur)


def modifier_mot_de_passe(utilisateur_id, nouveau_mot_de_passe):
    """Modifier le mot de passe d'un utilisateur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        password_hash = hasher_mot_de_passe(nouveau_mot_de_passe)
        curseur.execute(
            "UPDATE utilisateurs SET password_hash = %s WHERE id = %s",
            (password_hash, utilisateur_id)
        )
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def modifier_role(utilisateur_id, nouveau_role):
    """Modifier le rôle d'un utilisateur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        if nouveau_role not in ('admin', 'user'):
            print("Rôle invalide. Utilisez 'admin' ou 'user'.")
            return False
        curseur.execute(
            "UPDATE utilisateurs SET role = %s WHERE id = %s",
            (nouveau_role, utilisateur_id)
        )
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def desactiver_utilisateur(utilisateur_id):
    """Désactiver un utilisateur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "UPDATE utilisateurs SET actif = FALSE WHERE id = %s",
            (utilisateur_id,)
        )
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la désactivation: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def activer_utilisateur(utilisateur_id):
    """Activer un utilisateur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            "UPDATE utilisateurs SET actif = TRUE WHERE id = %s",
            (utilisateur_id,)
        )
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'activation: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def supprimer_utilisateur(utilisateur_id):
    """Supprimer un utilisateur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("DELETE FROM utilisateurs WHERE id = %s", (utilisateur_id,))
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)

"""
CRUD pour la table produits
"""

from connexion import get_connexion, get_curseur, fermer_connexion


def creer_produit(reference, nom, prix_unitaire, description=None, 
                  quantite_stock=0, seuil_alerte=10, categorie_id=None, fournisseur_id=None):
    """Créer un nouveau produit"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute(
            """INSERT INTO produits 
               (reference, nom, description, prix_unitaire, quantite_stock, 
                seuil_alerte, categorie_id, fournisseur_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (reference, nom, description, prix_unitaire, quantite_stock, 
             seuil_alerte, categorie_id, fournisseur_id)
        )
        produit_id = curseur.fetchone()[0]
        conn.commit()
        return produit_id
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création: {e}")
        return None
    finally:
        fermer_connexion(conn, curseur)


def lire_produits():
    """Lire tous les produits avec catégorie et fournisseur"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("""
            SELECT p.id, p.reference, p.nom, p.description, p.prix_unitaire, 
                   p.quantite_stock, p.seuil_alerte, c.nom as categorie, f.nom as fournisseur
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
            ORDER BY p.nom
        """)
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def lire_produit(produit_id):
    """Lire un produit par son ID"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("""
            SELECT p.id, p.reference, p.nom, p.description, p.prix_unitaire, 
                   p.quantite_stock, p.seuil_alerte, c.nom as categorie, f.nom as fournisseur,
                   p.categorie_id, p.fournisseur_id
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
            WHERE p.id = %s
        """, (produit_id,))
        return curseur.fetchone()
    finally:
        fermer_connexion(conn, curseur)


def lire_produit_par_reference(reference):
    """Lire un produit par sa référence"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("""
            SELECT p.id, p.reference, p.nom, p.description, p.prix_unitaire, 
                   p.quantite_stock, p.seuil_alerte, c.nom as categorie, f.nom as fournisseur
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
            WHERE p.reference = %s
        """, (reference,))
        return curseur.fetchone()
    finally:
        fermer_connexion(conn, curseur)


def rechercher_produits(terme):
    """Rechercher des produits par nom ou référence"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        pattern = f"%{terme}%"
        curseur.execute("""
            SELECT p.id, p.reference, p.nom, p.description, p.prix_unitaire, 
                   p.quantite_stock, p.seuil_alerte, c.nom as categorie, f.nom as fournisseur
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
            WHERE p.nom ILIKE %s OR p.reference ILIKE %s
            ORDER BY p.nom
        """, (pattern, pattern))
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def modifier_produit(produit_id, **kwargs):
    """Modifier un produit existant"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        champs_autorises = ['reference', 'nom', 'description', 'prix_unitaire', 
                           'quantite_stock', 'seuil_alerte', 'categorie_id', 'fournisseur_id']
        updates = []
        values = []
        
        for champ, valeur in kwargs.items():
            if champ in champs_autorises and valeur is not None:
                updates.append(f"{champ} = %s")
                values.append(valeur)
        
        if not updates:
            return False
        
        values.append(produit_id)
        query = f"UPDATE produits SET {', '.join(updates)} WHERE id = %s"
        curseur.execute(query, values)
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def supprimer_produit(produit_id):
    """Supprimer un produit"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("DELETE FROM produits WHERE id = %s", (produit_id,))
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)


def produits_en_alerte():
    """Obtenir les produits dont le stock est sous le seuil d'alerte"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("""
            SELECT p.id, p.reference, p.nom, p.quantite_stock, p.seuil_alerte,
                   c.nom as categorie
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            WHERE p.quantite_stock <= p.seuil_alerte
            ORDER BY p.quantite_stock
        """)
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def produits_par_categorie(categorie_id):
    """Obtenir les produits d'une catégorie"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("""
            SELECT p.id, p.reference, p.nom, p.prix_unitaire, p.quantite_stock
            FROM produits p
            WHERE p.categorie_id = %s
            ORDER BY p.nom
        """, (categorie_id,))
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)

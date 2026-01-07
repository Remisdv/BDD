"""
CRUD pour la table mouvements_stock
"""

from connexion import get_connexion, get_curseur, fermer_connexion


def entree_stock(produit_id, quantite, motif=None):
    """Enregistrer une entrée de stock"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        # Créer le mouvement
        curseur.execute(
            """INSERT INTO mouvements_stock (produit_id, type_mouvement, quantite, motif) 
               VALUES (%s, 'ENTREE', %s, %s) RETURNING id""",
            (produit_id, quantite, motif)
        )
        mouvement_id = curseur.fetchone()[0]
        
        # Mettre à jour le stock du produit
        curseur.execute(
            "UPDATE produits SET quantite_stock = quantite_stock + %s WHERE id = %s",
            (quantite, produit_id)
        )
        
        conn.commit()
        return mouvement_id
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'entrée de stock: {e}")
        return None
    finally:
        fermer_connexion(conn, curseur)


def sortie_stock(produit_id, quantite, motif=None):
    """Enregistrer une sortie de stock"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        # Vérifier le stock disponible
        curseur.execute(
            "SELECT quantite_stock FROM produits WHERE id = %s",
            (produit_id,)
        )
        result = curseur.fetchone()
        
        if not result:
            print("Produit non trouvé")
            return None
        
        stock_actuel = result[0]
        if stock_actuel < quantite:
            print(f"Stock insuffisant. Disponible: {stock_actuel}")
            return None
        
        # Créer le mouvement
        curseur.execute(
            """INSERT INTO mouvements_stock (produit_id, type_mouvement, quantite, motif) 
               VALUES (%s, 'SORTIE', %s, %s) RETURNING id""",
            (produit_id, quantite, motif)
        )
        mouvement_id = curseur.fetchone()[0]
        
        # Mettre à jour le stock du produit
        curseur.execute(
            "UPDATE produits SET quantite_stock = quantite_stock - %s WHERE id = %s",
            (quantite, produit_id)
        )
        
        conn.commit()
        return mouvement_id
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la sortie de stock: {e}")
        return None
    finally:
        fermer_connexion(conn, curseur)


def lire_mouvements(limite=50):
    """Lire les derniers mouvements de stock"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("""
            SELECT m.id, p.reference, p.nom, m.type_mouvement, m.quantite, 
                   m.motif, m.date_mouvement
            FROM mouvements_stock m
            JOIN produits p ON m.produit_id = p.id
            ORDER BY m.date_mouvement DESC
            LIMIT %s
        """, (limite,))
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def historique_produit(produit_id):
    """Obtenir l'historique des mouvements d'un produit"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("""
            SELECT m.id, m.type_mouvement, m.quantite, m.motif, m.date_mouvement
            FROM mouvements_stock m
            WHERE m.produit_id = %s
            ORDER BY m.date_mouvement DESC
        """, (produit_id,))
        return curseur.fetchall()
    finally:
        fermer_connexion(conn, curseur)


def supprimer_mouvement(mouvement_id):
    """Supprimer un mouvement (attention: ne recalcule pas le stock)"""
    conn = get_connexion()
    curseur = get_curseur(conn)
    try:
        curseur.execute("DELETE FROM mouvements_stock WHERE id = %s", (mouvement_id,))
        conn.commit()
        return curseur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        fermer_connexion(conn, curseur)

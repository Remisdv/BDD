"""
Application principale de gestion de stock
Menu interactif en console
"""

import os
import sys
from tabulate import tabulate

# Import des modules CRUD
from connexion import test_connexion
from categorie import (creer_categorie, lire_categories, lire_categorie, 
                       modifier_categorie, supprimer_categorie)
from fournisseur import (creer_fournisseur, lire_fournisseurs, lire_fournisseur,
                         modifier_fournisseur, supprimer_fournisseur)
from produit import (creer_produit, lire_produits, lire_produit, modifier_produit,
                     supprimer_produit, rechercher_produits, produits_en_alerte,
                     produits_par_categorie)
from mouvement import (entree_stock, sortie_stock, lire_mouvements, historique_produit)
from utilisateur import (authentifier, creer_utilisateur, lire_utilisateurs,
                         modifier_mot_de_passe, desactiver_utilisateur, compter_utilisateurs, admin_existe)


# Variable globale pour l'utilisateur connecté
utilisateur_connecte = None


def clear_screen():
    """Effacer l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause avant de continuer"""
    input("\nAppuyez sur Entrée pour continuer...")


def afficher_titre(titre):
    """Afficher un titre formaté"""
    print("\n" + "=" * 60)
    print(f"  {titre}")
    print("=" * 60)


def saisie_int(message, defaut=None):
    """Saisie sécurisée d'un entier"""
    while True:
        valeur = input(message)
        if valeur == "" and defaut is not None:
            return defaut
        try:
            return int(valeur)
        except ValueError:
            print("Veuillez entrer un nombre valide.")


def saisie_float(message, defaut=None):
    """Saisie sécurisée d'un float"""
    while True:
        valeur = input(message)
        if valeur == "" and defaut is not None:
            return defaut
        try:
            return float(valeur)
        except ValueError:
            print("Veuillez entrer un nombre valide.")


def selectionner_element(liste, message="Votre choix"):
    """
    Sélectionner un élément par son numéro dans une liste.
    Retourne l'UUID (premier élément du tuple) ou None.
    """
    if not liste:
        return None
    
    while True:
        choix = input(f"\n{message} (1-{len(liste)}, 0=annuler): ")
        if choix == "0" or choix == "":
            return None
        try:
            index = int(choix) - 1
            if 0 <= index < len(liste):
                return liste[index][0]  # Retourne l'UUID
            print(f"Entrez un nombre entre 1 et {len(liste)}")
        except ValueError:
            print("Veuillez entrer un nombre valide.")


# ============================================
# MENUS
# ============================================

def menu_principal():
    """Menu principal de l'application"""
    while True:
        clear_screen()
        afficher_titre("GESTION DE STOCK - Menu Principal")
        print(f"\nConnecté: {utilisateur_connecte[1]} ({utilisateur_connecte[2]})")
        print("\n1. Gestion des Produits")
        print("2. Gestion des Catégories")
        print("3. Gestion des Fournisseurs")
        print("4. Mouvements de Stock")
        print("5. Alertes Stock")
        if utilisateur_connecte[2] == 'admin':
            print("6. Gestion des Utilisateurs")
        print("0. Déconnexion")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            menu_produits()
        elif choix == "2":
            menu_categories()
        elif choix == "3":
            menu_fournisseurs()
        elif choix == "4":
            menu_mouvements()
        elif choix == "5":
            afficher_alertes_stock()
        elif choix == "6" and utilisateur_connecte[2] == 'admin':
            menu_utilisateurs()
        elif choix == "0":
            print("\nDéconnexion...")
            return


# ============================================
# MENU PRODUITS
# ============================================

def menu_produits():
    """Menu de gestion des produits"""
    while True:
        clear_screen()
        afficher_titre("Gestion des Produits")
        print("\n1. Lister tous les produits")
        print("2. Rechercher un produit")
        print("3. Ajouter un produit")
        print("4. Modifier un produit")
        print("5. Supprimer un produit")
        print("6. Voir détails d'un produit")
        print("0. Retour")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            lister_produits()
        elif choix == "2":
            rechercher_produit_menu()
        elif choix == "3":
            ajouter_produit()
        elif choix == "4":
            modifier_produit_menu()
        elif choix == "5":
            supprimer_produit_menu()
        elif choix == "6":
            voir_produit()
        elif choix == "0":
            return


def afficher_produits_tableau(produits, avec_numero=True):
    """Affiche les produits dans un tableau formaté"""
    if not produits:
        print("\nAucun produit trouvé.")
        return
    
    if avec_numero:
        headers = ["#", "Réf.", "Nom", "Prix", "Stock", "Seuil", "Catégorie", "Fournisseur"]
        data = [[i+1, p[1], p[2], f"{p[3]}€", p[4], p[5], p[6] or "-", p[7] or "-"] 
                for i, p in enumerate(produits)]
    else:
        headers = ["Réf.", "Nom", "Prix", "Stock", "Seuil", "Catégorie", "Fournisseur"]
        data = [[p[1], p[2], f"{p[3]}€", p[4], p[5], p[6] or "-", p[7] or "-"] 
                for p in produits]
    
    print(tabulate(data, headers=headers, tablefmt="grid"))


def lister_produits():
    """Afficher la liste des produits"""
    clear_screen()
    afficher_titre("Liste des Produits")
    produits = lire_produits()
    afficher_produits_tableau(produits)
    pause()


def rechercher_produit_menu():
    """Rechercher des produits"""
    clear_screen()
    afficher_titre("Rechercher un Produit")
    terme = input("\nTerme de recherche (nom ou référence): ")
    
    if terme:
        produits = rechercher_produits(terme)
        afficher_produits_tableau(produits)
    pause()


def ajouter_produit():
    """Ajouter un nouveau produit"""
    clear_screen()
    afficher_titre("Ajouter un Produit")
    
    # Afficher les catégories disponibles
    print("\nCatégories disponibles:")
    categories = lire_categories()
    if categories:
        data = [[i+1, c[1], c[2] or "-"] for i, c in enumerate(categories)]
        print(tabulate(data, headers=["#", "Nom", "Description"], tablefmt="simple"))
    
    # Afficher les fournisseurs disponibles
    print("\nFournisseurs disponibles:")
    fournisseurs = lire_fournisseurs()
    if fournisseurs:
        data = [[i+1, f[1]] for i, f in enumerate(fournisseurs)]
        print(tabulate(data, headers=["#", "Nom"], tablefmt="simple"))
    
    print("\n--- Informations du produit ---")
    reference = input("Référence: ")
    nom = input("Nom: ")
    description = input("Description (optionnel): ") or None
    prix = saisie_float("Prix unitaire: ")
    quantite = saisie_int("Quantité initiale (défaut: 0): ", 0)
    seuil = saisie_int("Seuil d'alerte (défaut: 10): ", 10)
    
    cat_id = selectionner_element(categories, "N° Catégorie") if categories else None
    four_id = selectionner_element(fournisseurs, "N° Fournisseur") if fournisseurs else None
    
    produit_id = creer_produit(reference, nom, prix, description, quantite, seuil, cat_id, four_id)
    
    if produit_id:
        print(f"\n✓ Produit créé avec succès")
    else:
        print("\n✗ Erreur lors de la création du produit")
    pause()


def modifier_produit_menu():
    """Modifier un produit existant"""
    clear_screen()
    afficher_titre("Modifier un Produit")
    
    produits = lire_produits()
    if not produits:
        print("\nAucun produit à modifier.")
        pause()
        return
    
    afficher_produits_tableau(produits)
    produit_id = selectionner_element(produits, "N° du produit à modifier")
    
    if not produit_id:
        return
    
    produit = lire_produit(produit_id)
    if not produit:
        print("\n✗ Produit non trouvé")
        pause()
        return
    
    print(f"\nProduit: {produit[2]} (Réf: {produit[1]})")
    print("Laissez vide pour conserver la valeur actuelle.\n")
    
    nom = input(f"Nom [{produit[2]}]: ") or None
    description = input(f"Description [{produit[3] or '-'}]: ") or None
    
    prix_input = input(f"Prix [{produit[4]}]: ")
    prix = float(prix_input) if prix_input else None
    
    seuil_input = input(f"Seuil d'alerte [{produit[6]}]: ")
    seuil = int(seuil_input) if seuil_input else None
    
    kwargs = {}
    if nom: kwargs['nom'] = nom
    if description: kwargs['description'] = description
    if prix: kwargs['prix_unitaire'] = prix
    if seuil: kwargs['seuil_alerte'] = seuil
    
    if kwargs and modifier_produit(produit_id, **kwargs):
        print("\n✓ Produit modifié avec succès")
    else:
        print("\n✗ Aucune modification effectuée")
    pause()


def supprimer_produit_menu():
    """Supprimer un produit"""
    clear_screen()
    afficher_titre("Supprimer un Produit")
    
    produits = lire_produits()
    if not produits:
        print("\nAucun produit à supprimer.")
        pause()
        return
    
    afficher_produits_tableau(produits)
    produit_id = selectionner_element(produits, "N° du produit à supprimer")
    
    if not produit_id:
        return
    
    produit = lire_produit(produit_id)
    print(f"\nProduit: {produit[2]} (Réf: {produit[1]})")
    confirm = input("Confirmer la suppression? (oui/non): ")
    
    if confirm.lower() == 'oui':
        if supprimer_produit(produit_id):
            print("\n✓ Produit supprimé avec succès")
        else:
            print("\n✗ Erreur lors de la suppression")
    else:
        print("\nSuppression annulée")
    pause()


def voir_produit():
    """Voir les détails d'un produit"""
    clear_screen()
    afficher_titre("Détails du Produit")
    
    produits = lire_produits()
    if not produits:
        print("\nAucun produit.")
        pause()
        return
    
    afficher_produits_tableau(produits)
    produit_id = selectionner_element(produits, "N° du produit à afficher")
    
    if not produit_id:
        return
    
    produit = lire_produit(produit_id)
    if produit:
        print(f"\n{'='*40}")
        print(f"Référence:    {produit[1]}")
        print(f"Nom:          {produit[2]}")
        print(f"Description:  {produit[3] or '-'}")
        print(f"Prix:         {produit[4]} €")
        print(f"Stock:        {produit[5]}")
        print(f"Seuil:        {produit[6]}")
        print(f"Catégorie:    {produit[7] or '-'}")
        print(f"Fournisseur:  {produit[8] or '-'}")
        print(f"{'='*40}")
        
        # Afficher l'historique des mouvements
        print("\nHistorique des mouvements:")
        mouvements = historique_produit(produit_id)
        if mouvements:
            headers = ["Type", "Qté", "Motif", "Date"]
            data = [[m[1], m[2], m[3] or "-", str(m[4])[:19]] for m in mouvements]
            print(tabulate(data, headers=headers, tablefmt="simple"))
        else:
            print("Aucun mouvement enregistré.")
    pause()


# ============================================
# MENU CATEGORIES
# ============================================

def menu_categories():
    """Menu de gestion des catégories"""
    while True:
        clear_screen()
        afficher_titre("Gestion des Catégories")
        print("\n1. Lister les catégories")
        print("2. Ajouter une catégorie")
        print("3. Modifier une catégorie")
        print("4. Supprimer une catégorie")
        print("5. Voir produits par catégorie")
        print("0. Retour")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            lister_categories_menu()
        elif choix == "2":
            ajouter_categorie()
        elif choix == "3":
            modifier_categorie_menu()
        elif choix == "4":
            supprimer_categorie_menu()
        elif choix == "5":
            voir_produits_categorie()
        elif choix == "0":
            return


def afficher_categories_tableau(categories):
    """Affiche les catégories dans un tableau"""
    if not categories:
        print("\nAucune catégorie trouvée.")
        return
    
    headers = ["#", "Nom", "Description"]
    data = [[i+1, c[1], c[2] or "-"] for i, c in enumerate(categories)]
    print(tabulate(data, headers=headers, tablefmt="grid"))


def lister_categories_menu():
    """Afficher la liste des catégories"""
    clear_screen()
    afficher_titre("Liste des Catégories")
    categories = lire_categories()
    afficher_categories_tableau(categories)
    pause()


def ajouter_categorie():
    """Ajouter une nouvelle catégorie"""
    clear_screen()
    afficher_titre("Ajouter une Catégorie")
    
    nom = input("Nom de la catégorie: ")
    description = input("Description (optionnel): ") or None
    
    cat_id = creer_categorie(nom, description)
    
    if cat_id:
        print(f"\n✓ Catégorie créée avec succès")
    else:
        print("\n✗ Erreur lors de la création")
    pause()


def modifier_categorie_menu():
    """Modifier une catégorie"""
    clear_screen()
    afficher_titre("Modifier une Catégorie")
    
    categories = lire_categories()
    if not categories:
        print("\nAucune catégorie à modifier.")
        pause()
        return
    
    afficher_categories_tableau(categories)
    cat_id = selectionner_element(categories, "N° de la catégorie à modifier")
    
    if not cat_id:
        return
    
    categorie = lire_categorie(cat_id)
    print(f"\nCatégorie: {categorie[1]}")
    nom = input(f"Nouveau nom [{categorie[1]}]: ") or None
    description = input(f"Nouvelle description [{categorie[2] or '-'}]: ") or None
    
    if modifier_categorie(cat_id, nom, description):
        print("\n✓ Catégorie modifiée avec succès")
    else:
        print("\n✗ Aucune modification effectuée")
    pause()


def supprimer_categorie_menu():
    """Supprimer une catégorie"""
    clear_screen()
    afficher_titre("Supprimer une Catégorie")
    
    categories = lire_categories()
    if not categories:
        print("\nAucune catégorie à supprimer.")
        pause()
        return
    
    afficher_categories_tableau(categories)
    cat_id = selectionner_element(categories, "N° de la catégorie à supprimer")
    
    if not cat_id:
        return
    
    categorie = lire_categorie(cat_id)
    print(f"\nCatégorie: {categorie[1]}")
    confirm = input("Confirmer la suppression? (oui/non): ")
    
    if confirm.lower() == 'oui':
        if supprimer_categorie(cat_id):
            print("\n✓ Catégorie supprimée avec succès")
        else:
            print("\n✗ Erreur lors de la suppression")
    pause()


def voir_produits_categorie():
    """Voir les produits d'une catégorie"""
    clear_screen()
    afficher_titre("Produits par Catégorie")
    
    categories = lire_categories()
    if not categories:
        print("\nAucune catégorie.")
        pause()
        return
    
    afficher_categories_tableau(categories)
    cat_id = selectionner_element(categories, "N° de la catégorie")
    
    if not cat_id:
        return
    
    produits = produits_par_categorie(cat_id)
    if produits:
        headers = ["#", "Réf.", "Nom", "Prix", "Stock"]
        data = [[i+1, p[1], p[2], f"{p[3]}€", p[4]] for i, p in enumerate(produits)]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("\nAucun produit dans cette catégorie.")
    pause()


# ============================================
# MENU FOURNISSEURS
# ============================================

def menu_fournisseurs():
    """Menu de gestion des fournisseurs"""
    while True:
        clear_screen()
        afficher_titre("Gestion des Fournisseurs")
        print("\n1. Lister les fournisseurs")
        print("2. Ajouter un fournisseur")
        print("3. Modifier un fournisseur")
        print("4. Supprimer un fournisseur")
        print("0. Retour")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            lister_fournisseurs_menu()
        elif choix == "2":
            ajouter_fournisseur()
        elif choix == "3":
            modifier_fournisseur_menu()
        elif choix == "4":
            supprimer_fournisseur_menu()
        elif choix == "0":
            return


def afficher_fournisseurs_tableau(fournisseurs):
    """Affiche les fournisseurs dans un tableau"""
    if not fournisseurs:
        print("\nAucun fournisseur trouvé.")
        return
    
    headers = ["#", "Nom", "Email", "Téléphone", "Adresse"]
    data = [[i+1, f[1], f[2] or "-", f[3] or "-", f[4] or "-"] 
            for i, f in enumerate(fournisseurs)]
    print(tabulate(data, headers=headers, tablefmt="grid"))


def lister_fournisseurs_menu():
    """Afficher la liste des fournisseurs"""
    clear_screen()
    afficher_titre("Liste des Fournisseurs")
    fournisseurs = lire_fournisseurs()
    afficher_fournisseurs_tableau(fournisseurs)
    pause()


def ajouter_fournisseur():
    """Ajouter un nouveau fournisseur"""
    clear_screen()
    afficher_titre("Ajouter un Fournisseur")
    
    nom = input("Nom du fournisseur: ")
    email = input("Email (optionnel): ") or None
    telephone = input("Téléphone (optionnel): ") or None
    adresse = input("Adresse (optionnel): ") or None
    
    four_id = creer_fournisseur(nom, email, telephone, adresse)
    
    if four_id:
        print(f"\n✓ Fournisseur créé avec succès")
    else:
        print("\n✗ Erreur lors de la création")
    pause()


def modifier_fournisseur_menu():
    """Modifier un fournisseur"""
    clear_screen()
    afficher_titre("Modifier un Fournisseur")
    
    fournisseurs = lire_fournisseurs()
    if not fournisseurs:
        print("\nAucun fournisseur à modifier.")
        pause()
        return
    
    afficher_fournisseurs_tableau(fournisseurs)
    four_id = selectionner_element(fournisseurs, "N° du fournisseur à modifier")
    
    if not four_id:
        return
    
    fournisseur = lire_fournisseur(four_id)
    print(f"\nFournisseur: {fournisseur[1]}")
    nom = input(f"Nom [{fournisseur[1]}]: ") or None
    email = input(f"Email [{fournisseur[2] or '-'}]: ") or None
    telephone = input(f"Téléphone [{fournisseur[3] or '-'}]: ") or None
    adresse = input(f"Adresse [{fournisseur[4] or '-'}]: ") or None
    
    if modifier_fournisseur(four_id, nom, email, telephone, adresse):
        print("\n✓ Fournisseur modifié avec succès")
    else:
        print("\n✗ Aucune modification effectuée")
    pause()


def supprimer_fournisseur_menu():
    """Supprimer un fournisseur"""
    clear_screen()
    afficher_titre("Supprimer un Fournisseur")
    
    fournisseurs = lire_fournisseurs()
    if not fournisseurs:
        print("\nAucun fournisseur à supprimer.")
        pause()
        return
    
    afficher_fournisseurs_tableau(fournisseurs)
    four_id = selectionner_element(fournisseurs, "N° du fournisseur à supprimer")
    
    if not four_id:
        return
    
    fournisseur = lire_fournisseur(four_id)
    print(f"\nFournisseur: {fournisseur[1]}")
    confirm = input("Confirmer la suppression? (oui/non): ")
    
    if confirm.lower() == 'oui':
        if supprimer_fournisseur(four_id):
            print("\n✓ Fournisseur supprimé avec succès")
        else:
            print("\n✗ Erreur lors de la suppression")
    pause()


# ============================================
# MENU MOUVEMENTS
# ============================================

def menu_mouvements():
    """Menu de gestion des mouvements de stock"""
    while True:
        clear_screen()
        afficher_titre("Mouvements de Stock")
        print("\n1. Entrée de stock")
        print("2. Sortie de stock")
        print("3. Historique des mouvements")
        print("0. Retour")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            faire_entree_stock()
        elif choix == "2":
            faire_sortie_stock()
        elif choix == "3":
            voir_historique()
        elif choix == "0":
            return


def faire_entree_stock():
    """Enregistrer une entrée de stock"""
    clear_screen()
    afficher_titre("Entrée de Stock")
    
    produits = lire_produits()
    if not produits:
        print("\nAucun produit.")
        pause()
        return
    
    print("\nProduits disponibles:")
    headers = ["#", "Réf.", "Nom", "Stock actuel"]
    data = [[i+1, p[1], p[2], p[4]] for i, p in enumerate(produits)]
    print(tabulate(data, headers=headers, tablefmt="simple"))
    
    produit_id = selectionner_element(produits, "N° du produit")
    if not produit_id:
        return
    
    quantite = saisie_int("Quantité à ajouter: ")
    motif = input("Motif (optionnel): ") or None
    
    mouv_id = entree_stock(produit_id, quantite, motif)
    
    if mouv_id:
        print(f"\n✓ Entrée de stock enregistrée")
    else:
        print("\n✗ Erreur lors de l'enregistrement")
    pause()


def faire_sortie_stock():
    """Enregistrer une sortie de stock"""
    clear_screen()
    afficher_titre("Sortie de Stock")
    
    produits = lire_produits()
    if not produits:
        print("\nAucun produit.")
        pause()
        return
    
    print("\nProduits disponibles:")
    headers = ["#", "Réf.", "Nom", "Stock actuel"]
    data = [[i+1, p[1], p[2], p[4]] for i, p in enumerate(produits)]
    print(tabulate(data, headers=headers, tablefmt="simple"))
    
    produit_id = selectionner_element(produits, "N° du produit")
    if not produit_id:
        return
    
    quantite = saisie_int("Quantité à retirer: ")
    motif = input("Motif (optionnel): ") or None
    
    mouv_id = sortie_stock(produit_id, quantite, motif)
    
    if mouv_id:
        print(f"\n✓ Sortie de stock enregistrée")
    else:
        print("\n✗ Erreur (stock insuffisant?)")
    pause()


def voir_historique():
    """Voir l'historique des mouvements"""
    clear_screen()
    afficher_titre("Historique des Mouvements")
    
    mouvements = lire_mouvements(50)
    
    if mouvements:
        headers = ["Réf.", "Produit", "Type", "Qté", "Motif", "Date"]
        data = [[m[1], m[2], m[3], m[4], m[5] or "-", str(m[6])[:19]] for m in mouvements]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("\nAucun mouvement enregistré.")
    pause()


# ============================================
# ALERTES STOCK
# ============================================

def afficher_alertes_stock():
    """Afficher les produits en alerte de stock"""
    clear_screen()
    afficher_titre("⚠️  ALERTES STOCK")
    
    produits = produits_en_alerte()
    
    if produits:
        headers = ["#", "Réf.", "Nom", "Stock", "Seuil", "Catégorie"]
        data = [[i+1, p[1], p[2], p[3], p[4], p[5] or "-"] for i, p in enumerate(produits)]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"\n⚠️  {len(produits)} produit(s) en alerte de stock!")
    else:
        print("\n✓ Aucun produit en alerte de stock.")
    pause()


# ============================================
# MENU UTILISATEURS (Admin)
# ============================================

def menu_utilisateurs():
    """Menu de gestion des utilisateurs (admin seulement)"""
    while True:
        clear_screen()
        afficher_titre("Gestion des Utilisateurs")
        print("\n1. Lister les utilisateurs")
        print("2. Créer un utilisateur")
        print("3. Modifier mot de passe")
        print("4. Désactiver un utilisateur")
        print("0. Retour")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            lister_utilisateurs_menu()
        elif choix == "2":
            creer_utilisateur_menu()
        elif choix == "3":
            modifier_mdp_menu()
        elif choix == "4":
            desactiver_utilisateur_menu()
        elif choix == "0":
            return


def afficher_utilisateurs_tableau(utilisateurs):
    """Affiche les utilisateurs dans un tableau"""
    if not utilisateurs:
        print("\nAucun utilisateur trouvé.")
        return
    
    headers = ["#", "Username", "Rôle", "Actif"]
    data = [[i+1, u[1], u[2], "Oui" if u[3] else "Non"] for i, u in enumerate(utilisateurs)]
    print(tabulate(data, headers=headers, tablefmt="grid"))


def lister_utilisateurs_menu():
    """Afficher la liste des utilisateurs"""
    clear_screen()
    afficher_titre("Liste des Utilisateurs")
    utilisateurs = lire_utilisateurs()
    afficher_utilisateurs_tableau(utilisateurs)
    pause()


def creer_utilisateur_menu():
    """Créer un nouvel utilisateur"""
    clear_screen()
    afficher_titre("Créer un Utilisateur")
    
    username = input("Nom d'utilisateur: ")
    mot_de_passe = input("Mot de passe: ")
    role = input("Rôle (admin/user) [user]: ") or 'user'
    
    if role not in ('admin', 'user'):
        role = 'user'
    
    user_id = creer_utilisateur(username, mot_de_passe, role)
    
    if user_id:
        print(f"\n✓ Utilisateur créé avec succès")
    else:
        print("\n✗ Erreur lors de la création")
    pause()


def modifier_mdp_menu():
    """Modifier le mot de passe d'un utilisateur"""
    clear_screen()
    afficher_titre("Modifier Mot de Passe")
    
    utilisateurs = lire_utilisateurs()
    if not utilisateurs:
        print("\nAucun utilisateur.")
        pause()
        return
    
    afficher_utilisateurs_tableau(utilisateurs)
    user_id = selectionner_element(utilisateurs, "N° de l'utilisateur")
    
    if not user_id:
        return
    
    nouveau_mdp = input("Nouveau mot de passe: ")
    
    if modifier_mot_de_passe(user_id, nouveau_mdp):
        print("\n✓ Mot de passe modifié avec succès")
    else:
        print("\n✗ Erreur lors de la modification")
    pause()


def desactiver_utilisateur_menu():
    """Désactiver un utilisateur"""
    clear_screen()
    afficher_titre("Désactiver un Utilisateur")
    
    utilisateurs = lire_utilisateurs()
    if not utilisateurs:
        print("\nAucun utilisateur.")
        pause()
        return
    
    afficher_utilisateurs_tableau(utilisateurs)
    user_id = selectionner_element(utilisateurs, "N° de l'utilisateur à désactiver")
    
    if not user_id:
        return
    
    if desactiver_utilisateur(user_id):
        print("\n✓ Utilisateur désactivé avec succès")
    else:
        print("\n✗ Erreur lors de la désactivation")
    pause()


# ============================================
# AUTHENTIFICATION & INSCRIPTION
# ============================================

def inscription():
    """Inscription d'un nouvel utilisateur"""
    clear_screen()
    afficher_titre("Inscription")
    
    print("\nCréation d'un nouveau compte")
    username = input("Nom d'utilisateur: ")
    
    if not username:
        print("\n✗ Le nom d'utilisateur est requis")
        pause()
        return False
    
    mot_de_passe = input("Mot de passe: ")
    if not mot_de_passe:
        print("\n✗ Le mot de passe est requis")
        pause()
        return False
    
    confirmer = input("Confirmer le mot de passe: ")
    if mot_de_passe != confirmer:
        print("\n✗ Les mots de passe ne correspondent pas")
        pause()
        return False
    
    # Premier utilisateur = admin, sinon user
    nb_users = compter_utilisateurs()
    role = 'admin' if nb_users == 0 else 'user'
    
    user_id = creer_utilisateur(username, mot_de_passe, role)
    
    if user_id:
        if role == 'admin':
            print(f"\n✓ Compte administrateur créé avec succès!")
        else:
            print(f"\n✓ Compte créé avec succès!")
        pause()
        return True
    else:
        print("\n✗ Erreur lors de la création du compte")
        pause()
        return False


def ecran_connexion():
    """Écran de connexion"""
    global utilisateur_connecte
    
    while True:
        clear_screen()
        afficher_titre("GESTION DE STOCK - Bienvenue")
        
        print("\n1. Se connecter")
        if not admin_existe():
            print("2. S'inscrire")
        print("0. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            username = input("\nNom d'utilisateur: ")
            mot_de_passe = input("Mot de passe: ")
            
            utilisateur = authentifier(username, mot_de_passe)
            
            if utilisateur:
                utilisateur_connecte = utilisateur
                print(f"\n✓ Bienvenue {utilisateur[1]}!")
                pause()
                menu_principal()
                utilisateur_connecte = None
            else:
                print("\n✗ Identifiants incorrects")
                pause()
        elif choix == "2" and not admin_existe():
            inscription()
        elif choix == "0":
            print("\nAu revoir!")
            sys.exit(0)


# ============================================
# POINT D'ENTRÉE
# ============================================

def main():
    """Point d'entrée de l'application"""
    print("Connexion à la base de données...")
    
    if not test_connexion():
        print("\n✗ Impossible de se connecter à la base de données.")
        print("Vérifiez que PostgreSQL est démarré et que les paramètres sont corrects.")
        sys.exit(1)
    
    print("✓ Connexion établie!")
    
    try:
        ecran_connexion()
    except KeyboardInterrupt:
        print("\n\nInterruption détectée. Au revoir!")
        sys.exit(0)


if __name__ == "__main__":
    main()

from app.database import SessionLocal
from app import models, schemas, crud
from datetime import date

def test_stock_flow():
    db = SessionLocal()
    try:
        # 1. Création d'une catégorie
        print("--- 1. Création d'une catégorie ---")
        import time
        ts = int(time.time())
        cat_name = f"Electronique-{ts}"
        cat_in = schemas.CategoryBase(category_name=cat_name)
        db_cat = crud.category_crud.create_category(db, cat_in)
        print(f"Catégorie créée: {db_cat.category_name} (ID: {db_cat.category_id})")

        # 2. Création d'un fournisseur
        print("\n--- 2. Création d'un fournisseur ---")
        sup_in = schemas.SupplierCreate(
            supplier_code=f"SUP-{ts}",
            supplier_name=f"Fournisseur Global-{ts}",
            address="456 Avenue Tech",
            phone="0987654321",
            email=f"contact-{ts}@sup.com",
            contact_per_name="Jean Tech",
            c_p_contact="0987654321",
            createby=1
        )
        db_sup = crud.supplier_crud.create_supplier(db, sup_in)
        print(f"Fournisseur créé: {db_sup.supplier_name} (ID: {db_sup.supplier_id})")

        # 3. Création d'un produit
        print("\n--- 3. Création d'un produit ---")
        prod_in = schemas.ProductCreate(
            product_code=f"PROD-{ts}",
            product_name=f"Article de Test-{ts}",
            category=cat_name,
            brand="Gen",
            unit="pcs",
            model="M1",
            product_details="Un article pour le test",
            purchase_price=100.0,
            retail_price=150.0,
            createby="admin",
            min_stock=10
        )
        db_prod = crud.product_crud.create_product(db, prod_in)
        print(f"Produit créé: {db_prod.product_name} (ID: {db_prod.product_id})")

        # 4. Création d'un mouvement de stock (Entrée de 50 unités)
        print("\n--- 4. Mouvement de Stock (Entrée de 50 unités) ---")
        import time
        ts = int(time.time())
        mv_in = schemas.StockMovementCreate(
            proposal_code=f"MV-{ts}-001",
            issue_code=f"ISS-{ts}-001",
            for_store_id=1,
            from_store_id=2, # Utilisation du magasin 2 comme "source"
            proposal_datetime=date.today(),
            proposal_by=1,
            issue_datetime=date.today(),
            issue_by=1,
            is_approved=True,
            is_received=True,
            details=[
                schemas.StockMovementDetailsBase(product_id=db_prod.product_id, received_qty=50)
            ]
        )
        db_mv = crud.stock_crud.create_movement(db, mv_in)
        print(f"Mouvement créé: {db_mv.proposal_code}")

        # 5. Vérification du stock en temps réel
        print("\n--- 5. Vérification du stock en temps réel ---")
        stocks = crud.stock_crud.get_store_stock(db, store_id=1)
        for s in stocks:
            if s.ProdID == db_prod.product_id:
                print(f"Stock pour le produit {db_prod.product_name} au Magasin 1: {s.current_stock}")

        # 6. Vérification des alertes
        print("\n--- 6. Vérification des alertes ---")
        # On crée un mouvement de sortie pour descendre en dessous de 10
        mv_out = schemas.StockMovementCreate(
            proposal_code=f"MV-{ts}-OUT",
            issue_code=f"ISS-{ts}-OUT",
            for_store_id=2,
            from_store_id=1,
            proposal_datetime=date.today(),
            proposal_by=1,
            issue_datetime=date.today(),
            issue_by=1,
            is_approved=True,
            is_received=True,
            details=[
                schemas.StockMovementDetailsBase(product_id=db_prod.product_id, received_qty=45)
            ]
        )
        crud.stock_crud.create_movement(db, mv_out)
        
        # Le stock devrait être de 5 (50 - 45), ce qui est en dessous du seuil de 10 (min_stock)
        alerts = crud.product_crud.get_stock_alerts(db, store_id=1)
        print(f"Produits en alerte au Magasin 1: {[p.product_name for p in alerts]}")

    except Exception as e:
        print(f"Erreur durant le test : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_stock_flow()

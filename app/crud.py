from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class CRUDCategory:
    def get_categories(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Category).offset(skip).limit(limit).all()

    def create_category(self, db: Session, category: schemas.CategoryBase):
        db_category = models.Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

class CRUDSupplier:
    def get_suppliers(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Supplier).offset(skip).limit(limit).all()

    def create_supplier(self, db: Session, supplier: schemas.SupplierCreate):
        db_supplier = models.Supplier(**supplier.dict())
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
        return db_supplier

class CRUDProduct:
    def get_product(self, db: Session, product_id: int):
        return db.query(models.Product).filter(models.Product.product_id == product_id).first()

    def get_products(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Product).offset(skip).limit(limit).all()

    def create_product(self, db: Session, product: schemas.ProductCreate):
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update_product(self, db: Session, product_id: int, product_update: schemas.ProductBase):
        db_product = self.get_product(db, product_id)
        if db_product:
            for var, value in vars(product_update).items():
                setattr(db_product, var, value) if value else None
            db_product.updatedate = datetime.utcnow()
            db.commit()
            db.refresh(db_product)
        return db_product

    def delete_product(self, db: Session, product_id: int):
        db_product = self.get_product(db, product_id)
        if db_product:
            db.delete(db_product)
            db.commit()
            return True
        return False

    def get_stock_alerts(self, db: Session, store_id: Optional[int] = None):
        # Cette méthode nécessite une jointure avec StoreStock pour être précise par magasin
        query = db.query(models.Product).join(models.StoreStock)
        if store_id:
            query = query.filter(models.StoreStock.StoreID == store_id)
        
        # Filtre les produits où (InQty - OutQty) <= min_stock
        return query.filter((models.StoreStock.InQty - models.StoreStock.OutQty) <= models.Product.min_stock).all()

class CRUDStock:
    def get_store_stock(self, db: Session, store_id: int):
        return db.query(models.StoreStock).filter(models.StoreStock.StoreID == store_id).all()

    def get_movements(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.StockMovement).offset(skip).limit(limit).all()

    def create_movement(self, db: Session, movement: schemas.StockMovementCreate):
        # 1. Créer l'entête du mouvement
        db_movement = models.StockMovement(
            proposal_code=movement.proposal_code,
            issue_code=movement.issue_code,
            for_store_id=movement.for_store_id,
            from_store_id=movement.from_store_id,
            proposal_datetime=movement.proposal_datetime,
            proposal_by=movement.proposal_by,
            issue_datetime=movement.issue_datetime,
            issue_by=movement.issue_by,
            is_approved=movement.is_approved,
            is_received=movement.is_received
        )
        db.add(db_movement)
        db.flush() # Pour obtenir l'ID

        # 2. Gérer les détails et mettre à jour le stock
        for detail in movement.details:
            db_detail = models.StockMovementDetails(
                movement_id=db_movement.movement_id,
                product_id=detail.product_id,
                received_qty=detail.received_qty
            )
            db.add(db_detail)

            # Mise à jour du stock réel (Entrée pour le magasin de destination)
            self._update_store_quantity(db, movement.for_store_id, detail.product_id, detail.received_qty, is_in=True)
            
            # Mise à jour du stock réel (Sortie pour le magasin d'origine)
            self._update_store_quantity(db, movement.from_store_id, detail.product_id, detail.received_qty, is_in=False)

        db.commit()
        db.refresh(db_movement)
        return db_movement

    def _update_store_quantity(self, db: Session, store_id: int, product_id: int, qty: int, is_in: bool):
        db_stock = db.query(models.StoreStock).filter(
            models.StoreStock.StoreID == store_id,
            models.StoreStock.ProdID == product_id
        ).first()

        if not db_stock:
            db_stock = models.StoreStock(StoreID=store_id, ProdID=product_id, InQty=0, OutQty=0)
            db.add(db_stock)

        if is_in:
            db_stock.InQty += qty
        else:
            db_stock.OutQty += qty
        
        db_stock.Stock_Date = datetime.utcnow()

class CRUDStore:
    def get_store(self, db: Session, store_id: int):
        return db.query(models.Store).filter(models.Store.store_id == store_id).first()

    def get_stores(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Store).offset(skip).limit(limit).all()

    def create_store(self, db: Session, store: schemas.StoreCreate):
        db_store = models.Store(
            store_name=store.store_name,
            store_code=store.store_code,
            store_phone=store.store_phone,
            store_address=store.store_address,
            createby=store.createby,
            isactive=store.isactive
        )
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store

    def update_store(self, db: Session, store_id: int, store_update: schemas.StoreUpdate):
        db_store = self.get_store(db, store_id)
        if db_store:
            update_data = store_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_store, key, value)
            db_store.updatedate = datetime.utcnow()
            db.commit()
            db.refresh(db_store)
        return db_store

class CRUDUser:
    def get_user(self, db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def create_user(self, db: Session, user: schemas.UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            password=hashed_password,
            is_admin=user.is_admin,
            store_id=user.store_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

# Instanciation des classes CRUD pour utilisation
user_crud = CRUDUser()
store_crud = CRUDStore()
category_crud = CRUDCategory()
supplier_crud = CRUDSupplier()
product_crud = CRUDProduct()
stock_crud = CRUDStock()

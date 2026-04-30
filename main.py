from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
from typing import List, Optional
from prometheus_fastapi_instrumentator import Instrumentator
import os

# Création des tables si elles n'existent pas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Multi Store Management POO (Python)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentation Prometheus
Instrumentator().instrument(app).expose(app)


@app.get("/api")
def read_root():
    return {"message": "Bienvenue dans l'API Multi Store (Python + POO)"}

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return crud.user_crud.create_user(db=db, user=user)

# Endpoints pour les magasins (Stores)
@app.post("/stores/", response_model=schemas.StoreResponse)
def create_store(store: schemas.StoreCreate, db: Session = Depends(database.get_db)):
    return crud.store_crud.create_store(db=db, store=store)

@app.get("/stores/", response_model=List[schemas.StoreResponse])
def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    stores = crud.store_crud.get_stores(db, skip=skip, limit=limit)
    return stores

@app.get("/stores/{store_id}", response_model=schemas.StoreResponse)
def read_store(store_id: int, db: Session = Depends(database.get_db)):
    db_store = crud.store_crud.get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Magasin non trouvé")
    return db_store

# --- Endpoints pour les Produits et Catégories ---
@app.post("/categories/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryBase, db: Session = Depends(database.get_db)):
    return crud.category_crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.CategoryResponse])
def read_categories(db: Session = Depends(database.get_db)):
    return crud.category_crud.get_categories(db=db)

@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.product_crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[schemas.ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.product_crud.get_products(db=db, skip=skip, limit=limit)

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductBase, db: Session = Depends(database.get_db)):
    db_product = crud.product_crud.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    success = crud.product_crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"message": "Produit supprimé"}

# --- Authentification ---
@app.post("/login", response_model=schemas.TokenResponse)
def login(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = crud.user_crud.get_user_by_email(db, login_data.email)
    if not user or not crud.pwd_context.verify(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    return {
        "access_token": "dummy-token-" + str(user.id),
        "token_type": "bearer",
        "user": user
    }

# --- Endpoints pour les Fournisseurs ---
@app.post("/suppliers/", response_model=schemas.SupplierResponse)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(database.get_db)):
    return crud.supplier_crud.create_supplier(db=db, supplier=supplier)

@app.get("/suppliers/", response_model=List[schemas.SupplierResponse])
def read_suppliers(db: Session = Depends(database.get_db)):
    return crud.supplier_crud.get_suppliers(db=db)

# --- Suivi des Stocks et Mouvements ---
@app.get("/stock/movements/", response_model=List[schemas.StockMovementResponse])
def read_movements(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.stock_crud.get_movements(db, skip=skip, limit=limit)

@app.post("/stock/movements/", response_model=schemas.StockMovementResponse)
def create_stock_movement(movement: schemas.StockMovementCreate, db: Session = Depends(database.get_db)):
    return crud.stock_crud.create_movement(db=db, movement=movement)

@app.get("/stock/status/{store_id}", response_model=List[schemas.StoreStockResponse])
def get_store_stock(store_id: int, db: Session = Depends(database.get_db)):
    return crud.stock_crud.get_store_stock(db=db, store_id=store_id)

@app.get("/stock/alerts/", response_model=List[schemas.ProductResponse])
def get_stock_alerts(store_id: Optional[int] = None, db: Session = Depends(database.get_db)):
    return crud.product_crud.get_stock_alerts(db=db, store_id=store_id)

# --- Service Visualisation (Dashboard) ---
# TOUJOURS À LA FIN pour ne pas bloquer les routes API
@app.get("/")
def read_dashboard():
    return FileResponse("dashboard.html")

# Montage pour les fichiers CSS, JS, etc.
app.mount("/", StaticFiles(directory="."), name="static")

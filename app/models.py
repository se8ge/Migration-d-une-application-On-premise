from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, BigInteger, Date, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Store(Base):
    __tablename__ = "store"

    store_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    store_name = Column(String(50), nullable=False)
    store_code = Column(String(3), nullable=False)
    store_phone = Column(String(50), nullable=False)
    store_address = Column(String(200), nullable=False)
    createby = Column(String(20), nullable=False)
    createdate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateby = Column(String(20), nullable=True)
    updatedate = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    isactive = Column(Boolean, default=True, nullable=False)

    # Relations
    users = relationship("User", back_populates="store")
    stocks = relationship("StoreStock", back_populates="store")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    status = Column(Integer, default=1)
    is_admin = Column(Boolean, default=False)
    store_id = Column(Integer, ForeignKey("store.store_id"), nullable=True)

    # Relations
    store = relationship("Store", back_populates="users")

    def get_full_name(self):
        """Exemple de méthode POO"""
        return f"{self.firstname} {self.lastname}"

class Category(Base):
    __tablename__ = "product_category"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(200), nullable=False, unique=True)
    isactive = Column(Boolean, default=True, nullable=False)

class Supplier(Base):
    __tablename__ = "supplier"

    supplier_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    supplier_code = Column(String(20), nullable=False)
    supplier_name = Column(String(200), nullable=False)
    address = Column(String(150), nullable=False)
    phone = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    contact_per_name = Column(String(50), nullable=False)
    c_p_contact = Column(String(30), nullable=False)
    isactive = Column(Boolean, default=True, nullable=False)
    createby = Column(Integer, nullable=False)
    createdate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateby = Column(Integer, nullable=False, default=0) # Ajout d'un défaut pour MySQL strict mode
    updatedate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Product(Base):
    __tablename__ = "product"

    product_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    product_code = Column(String(20), nullable=False)
    product_name = Column(String(200), nullable=False)
    category = Column(String(30), nullable=False)
    brand = Column(String(30), nullable=False)
    unit = Column(String(30), nullable=False)
    model = Column(String(50), nullable=False)
    product_details = Column(String(250), nullable=False)
    purchase_price = Column(Float, default=0.0, nullable=False)
    minimum_price = Column(Float, default=0.0, nullable=False)
    retail_price = Column(Float, default=0.0, nullable=False)
    block_price = Column(Float, default=0.0, nullable=False)
    isactive = Column(Boolean, default=True, nullable=False)
    createby = Column(String(20), nullable=False)
    createdate = Column(DateTime, default=datetime.utcnow, nullable=False)
    updateby = Column(String(20), nullable=False, default="admin")
    updatedate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Seuil d'alerte (Optionnel, ajouté pour répondre au besoin d'alerte)
    min_stock = Column(Integer, default=5, nullable=False)

class StockMovement(Base):
    __tablename__ = "stock_movement"

    movement_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    proposal_code = Column(String(20), nullable=False, unique=True)
    issue_code = Column(String(20), nullable=True, unique=True)
    for_store_id = Column(Integer, ForeignKey("store.store_id"), nullable=False)
    from_store_id = Column(Integer, ForeignKey("store.store_id"), nullable=False)
    proposal_datetime = Column(Date, nullable=False)
    proposal_by = Column(Integer, nullable=False)
    issue_datetime = Column(Date, nullable=False)
    issue_by = Column(Integer, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    is_received = Column(Boolean, default=False, nullable=False)

    # Relations
    details = relationship("StockMovementDetails", back_populates="movement")
    for_store = relationship("Store", foreign_keys=[for_store_id])
    from_store = relationship("Store", foreign_keys=[from_store_id])

class StockMovementDetails(Base):
    __tablename__ = "stock_movement_details"

    movement_id = Column(Integer, ForeignKey("stock_movement.movement_id"), primary_key=True)
    product_id = Column(BigInteger, ForeignKey("product.product_id"), primary_key=True)
    received_qty = Column(Integer, nullable=False)

    # Relations
    movement = relationship("StockMovement", back_populates="details")
    product = relationship("Product")

class StoreStock(Base):
    __tablename__ = "tmp_store_stock"

    StoreID = Column(Integer, ForeignKey("store.store_id"), primary_key=True)
    ProdID = Column(BigInteger, ForeignKey("product.product_id"), primary_key=True)
    InQty = Column(Integer, default=0, nullable=False)
    OutQty = Column(Integer, default=0, nullable=False)
    Stock_Date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    store = relationship("Store", back_populates="stocks")
    product = relationship("Product")

    @property
    def current_stock(self):
        return self.InQty - self.OutQty

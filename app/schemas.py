from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

# Schémas pour Store
class StoreBase(BaseModel):
    store_name: str
    store_code: str
    store_phone: str
    store_address: str
    isactive: bool = True

class StoreCreate(StoreBase):
    createby: str

class StoreUpdate(BaseModel):
    store_name: Optional[str] = None
    store_phone: Optional[str] = None
    store_address: Optional[str] = None
    updateby: str
    isactive: Optional[bool] = None

class StoreResponse(StoreBase):
    store_id: int
    createdate: datetime
    updatedate: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schémas pour User
class UserBase(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    is_admin: bool = False
    store_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    status: int

    class Config:
        from_attributes = True

# Schémas pour Category
class CategoryBase(BaseModel):
    category_name: str
    isactive: bool = True

class CategoryResponse(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True

# Schémas pour Supplier
class SupplierBase(BaseModel):
    supplier_code: str
    supplier_name: str
    address: str
    phone: str
    email: EmailStr
    contact_per_name: str
    c_p_contact: str
    isactive: bool = True

class SupplierCreate(SupplierBase):
    createby: int

class SupplierResponse(SupplierBase):
    supplier_id: int
    createdate: datetime
    updatedate: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schémas pour Product
class ProductBase(BaseModel):
    product_code: str
    product_name: str
    category: str
    brand: str
    unit: str
    model: str
    product_details: str
    purchase_price: float
    retail_price: float
    isactive: bool = True
    min_stock: int = 5

class ProductCreate(ProductBase):
    createby: str

class ProductResponse(ProductBase):
    product_id: int
    createdate: datetime
    updatedate: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schémas pour Stock Movement
class StockMovementDetailsBase(BaseModel):
    product_id: int
    received_qty: int

class StockMovementBase(BaseModel):
    proposal_code: str
    issue_code: Optional[str] = None
    for_store_id: int
    from_store_id: int
    proposal_datetime: date
    proposal_by: int
    issue_datetime: date
    issue_by: int
    is_approved: bool = False
    is_received: bool = False

class StockMovementCreate(StockMovementBase):
    details: List[StockMovementDetailsBase]

class StockMovementResponse(StockMovementBase):
    movement_id: int
    details: List[StockMovementDetailsBase]

    class Config:
        from_attributes = True

# Schémas pour Store Stock
class StoreStockResponse(BaseModel):
    StoreID: int
    ProdID: int
    InQty: int
    OutQty: int
    current_stock: int
    Stock_Date: datetime

    class Config:
        from_attributes = True

# Schémas pour l'Authentification
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

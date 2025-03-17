from sqlalchemy import Integer,String,ForeignKey,Boolean,TIMESTAMP,func,Text,Enum,Float,DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional,List
from datetime import datetime
from config.database import Base
from config.enums import RoleType,OrderStatus,PaymentMethod,PaymentStatus



class RoleTable(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True,index=True)
    role_name: Mapped[RoleType] = mapped_column(Enum(RoleType),nullable=False,unique=True)
    desc: Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(), onupdate=func.now(),nullable=False)
    users: Mapped[List["UserTable"]] = relationship(
        "UserTable",
        secondary="user_roles",
        back_populates="roles",
        foreign_keys="[UserRoles.user_id, UserRoles.role_id]"
    )
    user_roles: Mapped[List["UserRoles"]] = relationship("UserRoles", back_populates="role")
    

class UserTable(Base):
    __tablename__ = 'users'

    id: Mapped[int]=mapped_column(autoincrement=True,primary_key=True)
    username:Mapped[str] = mapped_column(String(100),nullable=False,unique=True) 
    password_hash:Mapped[str] = mapped_column(String(255),nullable=True)
    first_name: Mapped[str] = mapped_column(String(100),nullable=True)
    last_name:Mapped[str] = mapped_column(String(100),nullable=True)
    email: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    phone_number: Mapped[str]= mapped_column(String(15),nullable=True)
    address: Mapped[str] = mapped_column(String(250),nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean,default=False,nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),onupdate=func.now(),nullable=False)
    payments: Mapped[List["PaymentTable"]] = relationship("PaymentTable", back_populates="user")
    orders: Mapped[List["OrderTable"]] = relationship("OrderTable", back_populates="user")
    carts: Mapped[List["CartTable"]] = relationship("CartTable", back_populates="user")
    otps = relationship("OTPModel", back_populates="user", cascade="all, delete-orphan")
    chat_messages: Mapped[List["ChatMessageTable"]] = relationship("ChatMessageTable", back_populates="user")
    conversations: Mapped[List["ConversationTable"]] = relationship("ConversationTable", back_populates="user")
    user_roles: Mapped[List["UserRoles"]] = relationship(
        "UserRoles",
        back_populates="user",
        foreign_keys="[UserRoles.user_id]"
    )
    roles: Mapped[List["RoleTable"]] = relationship(
        "RoleTable",
        secondary="user_roles",
        back_populates="users",
        foreign_keys="[UserRoles.user_id, UserRoles.role_id]"
    )


class UserRoles(Base):
    __tablename__ = 'user_roles'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    assigned_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    user: Mapped["UserTable"] = relationship(
        "UserTable",
        foreign_keys="[UserRoles.user_id]",
        back_populates="user_roles"
    )
    role: Mapped["RoleTable"] = relationship(
        "RoleTable",
        foreign_keys="[UserRoles.role_id]",
        back_populates="user_roles"
    )


class CategoriesTable(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False,unique=True,index=True)
    desc: Mapped[str]  = mapped_column(Text,nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),nullable=False)
    products: Mapped[List["ProductTable"]] = relationship("ProductTable", back_populates="category")
    subcategories: Mapped[List["SubCategoriesTable"]] = relationship("SubCategoriesTable", back_populates="category")


class SubCategoriesTable(Base):
    __tablename__ = 'subcategories'

    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[str]  = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(Integer,ForeignKey(CategoriesTable.id),nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),nullable=False)
    category: Mapped["CategoriesTable"] = relationship("CategoriesTable",back_populates="subcategories")
    products: Mapped["ProductTable"] = relationship("ProductTable",back_populates="subcategory")


class ProductTable(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String(100),index=True,nullable=False)
    category_id:Mapped[int] = mapped_column(Integer,ForeignKey(CategoriesTable.id),nullable=False,index=True)
    subcategory_id:Mapped[int] = mapped_column(Integer,ForeignKey(SubCategoriesTable.id),nullable=False,index=True)
    desc: Mapped[str]  = mapped_column(Text,nullable=True)
    price: Mapped[float] = mapped_column(Float,nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer,nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),onupdate=func.now(),nullable=False)
    category:Mapped["CategoriesTable"] = relationship("CategoriesTable",back_populates="products")
    subcategory: Mapped["SubCategoriesTable"] = relationship("SubCategoriesTable",back_populates="products")
    discounts: Mapped[List["DiscountTable"]] = relationship("DiscountTable", back_populates="product", cascade="all, delete-orphan")


class DiscountTable(Base):
    __tablename__ = 'discounts'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False,index=True)
    discount_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    valid_from: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    valid_to: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True,index=True)

    product: Mapped["ProductTable"] = relationship("ProductTable", back_populates="discounts")


class CartTable(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserTable.id), nullable=False) 
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    user: Mapped["UserTable"] = relationship("UserTable", back_populates="carts")
    items: Mapped[List["CartItemTable"]] = relationship("CartItemTable", back_populates="cart", cascade="all, delete-orphan")



class CartItemTable(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)    
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey(ProductTable.id), nullable=False)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey(UserTable.id),nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    product: Mapped["ProductTable"] = relationship("ProductTable")   
    cart: Mapped["CartTable"] = relationship("CartTable",back_populates="items")
    


class OrderTable(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,index=True)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus),default=OrderStatus.PENDING,nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserTable.id),nullable=False,index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    address: Mapped[str] = mapped_column(String,nullable=False)
    user: Mapped["UserTable"] = relationship("UserTable", back_populates="orders")
    order_items: Mapped[List["OrderItemTable"]] = relationship("OrderItemTable", back_populates="order",cascade="all, delete-orphan")
    payment: Mapped[List["PaymentTable"]]= relationship("PaymentTable",back_populates="orders")

    coupon_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('coupons.id'), nullable=True)
    coupon: Mapped["CouponsTable"] = relationship("CouponsTable", back_populates="orders")



class OrderItemTable(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey(OrderTable.id),nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey(ProductTable.id),nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped["OrderTable"] = relationship("OrderTable", back_populates="order_items")
    product: Mapped["ProductTable"] = relationship("ProductTable")


class PaymentTable(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer,ForeignKey(OrderTable.id),nullable=False)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey(UserTable.id),nullable=False,index=True)
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod),nullable=False)
    payment_amount: Mapped[float] = mapped_column(Float,nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus),nullable=False)
    transction_id: Mapped[str] = mapped_column(String(250),unique=True,nullable=False,index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(),nullable=False)
    user: Mapped["UserTable"] = relationship("UserTable",back_populates="payments")  
    orders: Mapped["OrderTable"] = relationship("OrderTable",back_populates="payment")

      

class OTPModel(Base):
    __tablename__ = 'otps'
    id:Mapped[int]=mapped_column( primary_key=True, index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    hashed_otp:Mapped[str]=mapped_column(String, nullable=False)
    expires_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user = relationship("UserTable", back_populates="otps")


class CouponsTable(Base):
    __tablename__ = 'coupons'

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True,index=True)
    code:Mapped[str] = mapped_column(String(50),nullable=False,unique=True,index=True)
    discount_percentage: Mapped[float] = mapped_column(Float,nullable=False)
    max_discount_amount:Mapped[Optional[float]] = mapped_column(Float,nullable=True)
    valid_from:Mapped[datetime] = mapped_column(TIMESTAMP,nullable=False)
    valid_to:Mapped[datetime]  = mapped_column(TIMESTAMP,nullable=False)
    min_purchase_amount:Mapped[Optional[float]] = mapped_column(Float,nullable=True)
    usage_limit:Mapped[int] = mapped_column(Integer,nullable=True,default=1)
    usage_count:Mapped[int] = mapped_column(Integer,nullable=False,default=0)
    is_active:Mapped[bool] = mapped_column(Boolean,default=True,index=True)
    orders: Mapped[List["OrderTable"]] = relationship("OrderTable", back_populates="coupon")
    
    
    
class ChatMessageTable(Base):
    __tablename__ = 'chat_messages'
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    agent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agents.id"), nullable=True)  # Optional for user-to-agent routing
    conversation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("conversations.id"), nullable=True)
    
    message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Nullable if only a file is sent
    file_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # For file attachments
    file_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Type of file (image, video, pdf, etc.)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # For notifications
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relationships
    user: Mapped[Optional["UserTable"]] = relationship("UserTable", back_populates="chat_messages")
    agent: Mapped[Optional["AgentTable"]] = relationship("AgentTable", back_populates="chat_messages")
    conversation: Mapped["ConversationTable"] = relationship("ConversationTable", back_populates="chat_messages")

    
class ConversationTable(Base):
    __tablename__ = 'conversations'
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    agent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agents.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    chat_messages: Mapped[List["ChatMessageTable"]] = relationship("ChatMessageTable", back_populates="conversation")
    user: Mapped[UserTable] = relationship("UserTable", back_populates="conversations")
    agent: Mapped[Optional["AgentTable"]] = relationship("AgentTable", back_populates="conversations")
    
class AgentTable(Base):
    __tablename__ = 'agents'
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Agent's name
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)  # Unique email for authentication
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    
    # Relationships
    chat_messages: Mapped[List["ChatMessageTable"]] = relationship("ChatMessageTable", back_populates="agent")
    conversations: Mapped[List["ConversationTable"]] = relationship("ConversationTable", back_populates="agent")
    
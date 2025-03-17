from enum import Enum as PyEnum



class RoleType(str,PyEnum):
    ADMIN = "Admin"
    CUSTOMER = "Customer"
    SELLER = "Seller"


class PaymentMethod(str,PyEnum):
    CREDIT_CARD = "Credit Card"
    PAYPAL = "PayPal"
    BANK_TRANSFER = "Bank Transfer"


class PaymentStatus(str,PyEnum):
    COMPLETED = "Complete"
    PENDING = "Pending"
    FAILED = "Failed"


class OrderStatus(str,PyEnum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "delivered"
    CANCELLED = "Cancelled"
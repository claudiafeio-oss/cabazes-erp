from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class MoveType(str, Enum):
    RECEIPT = "receipt"
    CONSUMPTION = "consumption"
    PRODUCTION = "production"
    ADJUSTMENT = "adjustment"
    RETURN = "return"
    ASSEMBLY_CONSUMPTION = "assembly_consumption"
    ASSEMBLY_OUTPUT = "assembly_output"


class ReferenceType(str, Enum):
    PURCHASE_RECEIPT = "purchase_receipt"
    ASSEMBLY_ORDER = "assembly_order"
    INVENTORY_ADJUSTMENT = "inventory_adjustment"
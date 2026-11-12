import uuid
import enum
from sqlalchemy import String, Boolean, Enum
from app.db.base import TimeStampMixin, Base
from sqlalchemy.orm import Mapped, mapped_column

class Role(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    role: Mapped[Role] = mapped_column(
        Enum(
            Role,
            native_enum=False,
            length=20,
            values_callable=lambda e: [m.value for m in e]
        ),
        default=Role.CUSTOMER,
        server_default=Role.CUSTOMER.value
    )

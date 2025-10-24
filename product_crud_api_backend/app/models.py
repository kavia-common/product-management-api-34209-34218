from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

# SQLAlchemy instance will be provided by app factory
db = SQLAlchemy()


class Product(db.Model):
    """Product model representing an item in inventory."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # PUBLIC_INTERFACE
    def to_dict(self) -> dict:
        """Serialize the Product model to a dictionary for JSON responses."""
        return {"id": self.id, "name": self.name, "price": float(self.price), "quantity": int(self.quantity)}

    def __repr__(self) -> str:  # pragma: no cover - for debug only
        return f"<Product id={self.id} name={self.name!r} price={self.price} qty={self.quantity}>"

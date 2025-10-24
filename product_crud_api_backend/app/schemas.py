from marshmallow import Schema, fields, validates, ValidationError


class ProductBaseSchema(Schema):
    """Base schema for shared product fields."""

    name = fields.String(required=True, description="Product name", metadata={"example": "Widget"})
    price = fields.Float(required=True, description="Product price", metadata={"example": 19.99})
    quantity = fields.Integer(required=True, description="Quantity in stock", metadata={"example": 5})

    @validates("price")
    def validate_price(self, value: float) -> None:
        if value is None or value < 0:
            raise ValidationError("Price must be a non-negative number.")

    @validates("quantity")
    def validate_quantity(self, value: int) -> None:
        if value is None or value < 0:
            raise ValidationError("Quantity must be a non-negative integer.")


class ProductCreateSchema(ProductBaseSchema):
    """Schema for creating a product."""
    # id is auto-generated; not accepted on input


class ProductUpdateSchema(Schema):
    """Schema for updating a product. All fields optional."""
    name = fields.String(required=False, description="Product name")
    price = fields.Float(required=False, description="Product price")
    quantity = fields.Integer(required=False, description="Quantity in stock")

    @validates("price")
    def validate_price(self, value: float) -> None:
        if value is not None and value < 0:
            raise ValidationError("Price must be a non-negative number.")

    @validates("quantity")
    def validate_quantity(self, value: int) -> None:
        if value is not None and value < 0:
            raise ValidationError("Quantity must be a non-negative integer.")


class ProductResponseSchema(Schema):
    """Schema for product response."""
    id = fields.Integer(required=True, description="Product ID")
    name = fields.String(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)


class ProductsListResponseSchema(Schema):
    """Schema for list response."""
    items = fields.List(fields.Nested(ProductResponseSchema), required=True)
    total = fields.Integer(required=True, description="Total number of products")

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func  # for aggregation
from ..models import db, Product
from ..schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema,
    ProductsListResponseSchema,
)

blp = Blueprint(
    "Products",
    "products",
    url_prefix="/products",
    description="CRUD endpoints for managing products",
)


@blp.route("/")
class ProductsCollection(MethodView):
    """Collection endpoints for products: list and create."""

    # PUBLIC_INTERFACE
    @blp.response(200, ProductsListResponseSchema)
    def get(self):
        """List all products.
        Returns:
          200: JSON object with items[] and total fields.
        """
        products = Product.query.order_by(Product.id.asc()).all()
        return {"items": [p.to_dict() for p in products], "total": len(products)}

    # PUBLIC_INTERFACE
    @blp.arguments(ProductCreateSchema, location="json")
    @blp.response(201, ProductResponseSchema)
    def post(self, json_data):
        """Create a product.
        Body:
          name (str, required), price (float >= 0), quantity (int >= 0)
        Returns:
          201: Created product JSON.
        Errors:
          400: Validation errors.
        """
        try:
            product = Product(
                name=json_data["name"].strip(),
                price=float(json_data["price"]),
                quantity=int(json_data["quantity"]),
            )
            db.session.add(product)
            db.session.commit()
            return product.to_dict()
        except SQLAlchemyError as exc:
            db.session.rollback()
            abort(500, message=f"Database error: {exc.__class__.__name__}")


@blp.route("/balance")
class ProductsBalance(MethodView):
    """Aggregate endpoint for total inventory balance."""

    # PUBLIC_INTERFACE
    @blp.response(200)
    def get(self):
        """Compute and return the total inventory balance.

        Returns:
          200: JSON object {"total_balance": number}
        Errors:
          500: On database errors.

        Notes:
          Uses SUM(price * quantity) across all products.
          Ensures JSON-safe numeric by converting to float.
        """
        try:
            # Build aggregation expression: price * quantity, then SUM()
            total = db.session.query(func.sum(Product.price * Product.quantity)).scalar()
            # If there are no rows, SUM returns None; treat as 0.0
            total_balance = float(total or 0.0)
            return {"total_balance": total_balance}
        except SQLAlchemyError as exc:
            abort(500, message=f"Database error: {exc.__class__.__name__}")


@blp.route("/<int:product_id>")
class ProductItem(MethodView):
    """Item endpoints for a single product."""

    # PUBLIC_INTERFACE
    @blp.response(200, ProductResponseSchema)
    def get(self, product_id: int):
        """Retrieve a single product by ID."""
        product = Product.query.get(product_id)
        if not product:
            abort(404, message="Product not found")
        return product.to_dict()

    # PUBLIC_INTERFACE
    @blp.arguments(ProductUpdateSchema, location="json")
    @blp.response(200, ProductResponseSchema)
    def put(self, json_data, product_id: int):
        """Update an existing product.
        Body: any of name, price, quantity
        Returns:
          200: Updated product JSON.
        """
        product = Product.query.get(product_id)
        if not product:
            abort(404, message="Product not found")
        try:
            if "name" in json_data and json_data["name"] is not None:
                product.name = json_data["name"].strip()
            if "price" in json_data and json_data["price"] is not None:
                product.price = float(json_data["price"])
            if "quantity" in json_data and json_data["quantity"] is not None:
                product.quantity = int(json_data["quantity"])
            db.session.commit()
            return product.to_dict()
        except SQLAlchemyError as exc:
            db.session.rollback()
            abort(500, message=f"Database error: {exc.__class__.__name__}")

    # PUBLIC_INTERFACE
    @blp.response(204)
    def delete(self, product_id: int):
        """Delete a product.
        Returns:
          204: No content on success.
        """
        product = Product.query.get(product_id)
        if not product:
            abort(404, message="Product not found")
        try:
            db.session.delete(product)
            db.session.commit()
            return "", 204
        except SQLAlchemyError as exc:
            db.session.rollback()
            abort(500, message=f"Database error: {exc.__class__.__name__}")

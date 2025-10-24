# Product CRUD API (Flask)

Flask-based REST API for managing products with SQLite persistence and OpenAPI docs.

## Quick start

- Install dependencies
  pip install -r requirements.txt

- Run the service (defaults to port 3001)
  python run.py

Docs available at: /docs

Health check:
- GET /

## Environment variables

- PORT: Port to bind (default: 3001)
- DATABASE_URL: SQLAlchemy DB URL (default: sqlite:///products.db)

Also see .env.example for a sample.

## Endpoints

- GET /products
  Returns list of products.
  curl -s http://localhost:${PORT:-3001}/products | jq .

- POST /products
  Creates a product (name, price, quantity).
  curl -s -X POST http://localhost:${PORT:-3001}/products \
    -H "Content-Type: application/json" \
    -d '{"name":"Widget","price":19.99,"quantity":5}'

- GET /products/{id}
  Retrieve a single product.
  curl -s http://localhost:${PORT:-3001}/products/1

- PUT /products/{id}
  Update fields (name, price, quantity).
  curl -s -X PUT http://localhost:${PORT:-3001}/products/1 \
    -H "Content-Type: application/json" \
    -d '{"price":24.99,"quantity":10}'

- DELETE /products/{id}
  Delete a product.
  curl -i -X DELETE http://localhost:${PORT:-3001}/products/1

## Validation and error handling

- 400 for validation errors with Marshmallow
- 404 when a product is not found
- 201 on create, 200 on read/update, 204 on delete

## Notes

- Uses SQLite by default and auto-creates tables on startup.
- To persist data across restarts, keep products.db file in the container folder.


# Endpoints previstos

## Health
- GET /health

## Auth
- POST /auth/login
- POST /auth/refresh

## Products
- GET /products
- POST /products
- GET /products/{id}
- PATCH /products/{id}

## Purchases
- GET /purchase-orders
- POST /purchase-orders
- POST /purchase-orders/{id}/confirm
- POST /purchase-orders/{id}/receive

## Baskets
- GET /baskets
- POST /baskets
- GET /baskets/{id}/availability

## Assemblies
- GET /assemblies
- POST /assemblies
- POST /assemblies/{id}/confirm
- POST /assemblies/{id}/complete

## Stock
- GET /stock/on-hand
- GET /stock/movements
- POST /stock/adjustments

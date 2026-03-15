from fastapi import FastAPI

from app.api import assemblies, auth, baskets, locations, lots, products, purchases, stock, suppliers

app = FastAPI(title="Cabazes ERP API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(locations.router)
app.include_router(lots.router)
app.include_router(stock.router)
app.include_router(suppliers.router)
app.include_router(purchases.router)
app.include_router(baskets.router)
app.include_router(assemblies.router)

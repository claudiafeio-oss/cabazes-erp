from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import assemblies, auth, baskets, locations, lots, products, purchases, stock, suppliers

app = FastAPI(title="Cabazes ERP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
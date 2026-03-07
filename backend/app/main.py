from fastapi import FastAPI

app = FastAPI(title="Cabazes ERP API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

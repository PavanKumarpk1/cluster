from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tinydb import TinyDB, Query
import uvicorn

app = FastAPI()
# Points directly to the products.json file copied into the root
db = TinyDB('products.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    name: str
    price: int
    image_url: str

# Aligned with frontend fetch requests and Ingress path rules
@app.get("/api/products/")
async def get_products():
    return db.all()

# ADD THIS: Health check endpoint for GCE Load Balancer
@app.get("/")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/products/")
async def add_product(product: Product):
    db.insert(product.dict())
    return {"message": "Product added successfully"}

@app.delete("/api/products/{name}")
async def delete_product(name: str):
    ProductQuery = Query()
    removed = db.remove(ProductQuery.name == name)
    if not removed:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)

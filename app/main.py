from fastapi import FastAPI
from app.database import Base, engine
from app.routers import plants, explore


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gardener Assistant API")


app.include_router(plants.router)
app.include_router(explore.router)

@app.get("/")
def root():
    return {"message": "Gardener Assistant API. Docs available at /docs"}

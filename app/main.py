from fastapi import FastAPI
from . import models
from . database import engine
from . routers import car, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(car.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Data": "Welcome to my CarStore !!!"}
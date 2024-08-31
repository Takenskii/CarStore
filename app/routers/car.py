from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from .. database import get_db
from typing import Optional, List

router = APIRouter(
    tags=['Cars']
)

@router.get("/cars", response_model=List[schemas.CarOut])
def get_cars(db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, model:Optional[str]="", year:Optional[str]=""):

    car = db.query(models.Car).filter(models.Car.brand.contains(model), models.Car.year.contains(year)).limit(limit).offset(skip).all()
    return car

@router.post("/cars", status_code=status.HTTP_201_CREATED, response_model=schemas.CarOut)
def create_cars(car: schemas.CarIn, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    print(current_user.id)
    new_car = models.Car(user_id=current_user.id, **car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

@router.get("/cars/{id}", response_model=schemas.CarOut)
def get_car(id: int, db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):

    car = db.query(models.Car).filter(models.Car.id == id).first()

    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"car with {id} was not found")
    
    return car

@router.delete("/cars/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cars(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
  
    car_query = db.query(models.Car).filter(models.Car.id == id)
    
    car = car_query.first()

    if car == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"car with id: {id} does not exist")
    if car.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="NOT AUTHORIZED TO PERFORM REQUESTED ACTION")

    car_query.delete(synchronize_session=False)
    db.commit()

@router.put("/cars/{id}", response_model=schemas.CarOut)
def update_car(id: int, updated_car: schemas.CarIn, db: Session = Depends(get_db), 
               current_user: int = Depends(oauth2.get_current_user)):
 
    car_query = db.query(models.Car).filter(models.Car.id == id)
    
    car = car_query.first()

    if car == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"car with id: {id} does not exist")
    if car.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="NOT AUTHORIZED TO PERFORM REQUESTED ACTION")    
    
    car_query.update(updated_car.dict(), synchronize_session=False)
    db.commit()
    return car_query.first()
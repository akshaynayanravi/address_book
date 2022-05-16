from audioop import add
from pydoc import describe
import re
from wsgiref.util import request_uri
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy import desc

from . import schemas, models

from .database import SessionLocal, engine

from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/address', status_code=status.HTTP_201_CREATED)
def create_address(request: schemas.AddressBase, db: Session = Depends(get_db)):
    name = request.name
    lattitude = request.lattitude
    longitude = request.longitude
    if request.description:
        description = request.description
    else:
        description = ""

    new_address = models.AddressBook(name=name, description=description,
                                     lattitude=lattitude, longitude=longitude)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return {
        "status": 200,
        "message": "Address created successfully.",
        "data": {
            "id": new_address.id,
            "name": new_address.name,
            "description": new_address.description,
            "lattitude": new_address.lattitude,
            "longitude": new_address.longitude
        }
    }


@app.get('/address', status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    addresses = db.query(models.AddressBook).all()
    if not addresses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No addresses found.")

    return addresses


@app.get('/address/{address_id}', status_code=status.HTTP_200_OK)
def get_user_details(address_id, db: Session = Depends(get_db)):
    address = db.query(models.AddressBook).filter(
        models.AddressBook.id == address_id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Address detail {address_id} not found.")

    return {
        "status": 200,
        "message": "Address fetched successfully.",
        "data": address
    }


@app.put('/address/{address_id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(address_id, request: schemas.AddressBase, db: Session = Depends(get_db)):
    address = db.query(models.AddressBook).filter(models.AddressBook.id == address_id)
    if not address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    request_data = request.dict(exclude_unset=True)
    address = address.first()
    for key, value in request_data.items():
        setattr(address, key, value)
    db.add(address)
    db.commit()
    db.refresh(address)

    return {
        "status": 202,
        "message": "Address updated successfully.",
        "data": address
    }


@app.delete('/address/{address_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(address_id, db: Session = Depends(get_db)):
    address = db.query(models.AddressBook).filter(models.AddressBook.id == address_id)
    if not address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    address.delete(synchronize_session=False)
    db.commit()

    return {
        "status": 204,
        "message": "Address deleted successfully.",
        "data": []
    }

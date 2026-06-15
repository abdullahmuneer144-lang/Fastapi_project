from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta , timezone
from jose import jwt , JWTError


SECRET_KEY = "my_key"
Algorithum = "HS256"
Expiring_time = 30

outh2_sehema= OAuth2PasswordBearer(tokenUrl="login")

def create_tokken(data:dict):
    to_encode = data.copy()

    expire= datetime.now(timezone.utc) + timedelta(minutes = Expiring_time)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm= Algorithum)

def verify_tokken(tokken:str= Depends(outh2_sehema)):
    try:
        paylod= jwt.decode(tokken,SECRET_KEY,algorithms= [Algorithum])
        return paylod
    except JWTError:
        raise HTTPException( status_code= 401, detail="Invalid tokken")







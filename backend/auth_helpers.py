from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from backend.auth import SECRET_KEY, ALGORITHM
from backend.models.user import User
from backend.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(lambda: SessionLocal())):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

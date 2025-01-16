from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token  # Relative import, assuming token.py is in the same directory as oauth2.py

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(data, credentials_exception)

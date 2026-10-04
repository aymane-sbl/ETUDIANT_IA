import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import jwt,JWTError
from dotenv import load_dotenv
from shared.errors.errors import AuthError
from shared.dependencies.redis import get_lang_in_redis

from fastapi.security import  OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status


load_dotenv(override=True)

# jwt
secret_key = os.getenv("SECRET_TOKEN")
def encode_token(payload:dict):
    token = jwt.encode(payload,secret_key,algorithm="HS256")
    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login",auto_error=False)
def decode_token(token:str = Depends(oauth2_scheme),lang = Depends(get_lang_in_redis)):
    try :
        # check token is none
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=lang["auth"]["token_missing"]
            )

        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=lang["auth"]["token_expired"])

# hash & verify password
PH = PasswordHasher()
def hash_password(password):
    return PH.hash(password)

def verify_password(lang,password, hashed_password):
    try :
        return  PH.verify(password=password,hash= hashed_password)
    except VerifyMismatchError:
        raise AuthError(lang["auth"]["wrong_password"])



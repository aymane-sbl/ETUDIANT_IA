from fastapi import APIRouter,Depends,HTTPException,status

from auth.services.auth_service import AuthService
from auth.schemas.auth_schemas import LoginSchemas,RegisterSchemas
from shared.dependencies.conn_db import get_connection_db
from shared.dependencies.redis import  get_lang_in_redis,get_redis_connection
from shared.errors.errors import AuthError, DbError, TooManyAttempts

router = APIRouter(prefix="/api/v1/auth",tags=["Auth"])

def get_auth_service(connection = Depends(get_connection_db),lang = Depends(get_lang_in_redis),redis = Depends(get_redis_connection)):
    return AuthService(connection=connection,lang=lang,redis=redis)

# register
@router.post("/regiter",status_code=status.HTTP_201_CREATED)
async def register(auth_schemas :RegisterSchemas ,auth_service: AuthService = Depends(get_auth_service)):
    try :
        result = await  auth_service.register(email=auth_schemas.email,password=auth_schemas.password)
        return result
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= str(e))
    except TooManyAttempts as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail= str(e))
    except DbError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail= str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail= "INTERNAL SERVER ERROR")

# login
@router.post("/login")
async def login(auth_schemas :LoginSchemas ,auth_service: AuthService = Depends(get_auth_service)):
    try :
        result = await  auth_service.login(email=auth_schemas.email,password=auth_schemas.password)
        return result
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= str(e))
    except TooManyAttempts as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail= str(e))
    except DbError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail= str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail= "INTERNAL SERVER ERROR")

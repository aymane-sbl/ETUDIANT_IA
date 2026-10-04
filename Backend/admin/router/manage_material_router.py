from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile, Query
from fastapi_cache import FastAPICache

from admin.services.manage_material_service import Manage_MaterialService
from admin.utils.check_admin import check_is_admin
from auth.utils.securite import  decode_token
from shared.dependencies.conn_db import get_connection_db
from shared.dependencies.redis import  get_lang_in_redis
from shared.errors.errors import DbError, S3UploadError, UnauthorizedError, MaterialError

router = APIRouter(prefix="/api/v1/admin/materials",tags=["Admin-Materials"])

# get materials obj
def get_material_service_obj(connection = Depends(get_connection_db),lang = Depends(get_lang_in_redis)):
    return Manage_MaterialService(connection=connection,lang=lang)
# add materials
@router.post("/",status_code=status.HTTP_201_CREATED)
async def add_material( payload : dict = Depends(decode_token),
                        material_service:Manage_MaterialService = Depends(get_material_service_obj),
                        subject_id : int = Form(...), semester : int = Form(...),
                        year_academic : str = Form(...), type : str = Form(...),
                        session : str = Form(...), file : UploadFile = File(...)
                       ):
    try :
        check_is_admin(role=payload["role"])
        result = await material_service.add_material(subject_id,semester,year_academic,type,session,file)
        await FastAPICache.clear(namespace="HOME_CACHE")
        await FastAPICache.clear(namespace="FILTER_CACHE")
        await FastAPICache.clear(namespace="SEARCH_CACHE")
        return result
    except UnauthorizedError as e :
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
    except S3UploadError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    except DbError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"INTERNAL_SERVER_ERROR")

@router.delete("/")
async def delete_materials(material_services : Manage_MaterialService  = Depends(get_material_service_obj),id : int  = Query(...,ge=1),) :
    try :
        result =await  material_services.delete_materials(id=id)
        return result
    except MaterialError as e :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except DbError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"INTERNAL_SERVER_ERROR")




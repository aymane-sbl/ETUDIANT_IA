from fastapi import APIRouter,Depends,HTTPException,status,Query,Path
from fastapi_cache.decorator import cache
from shared.errors.errors import DbError, SearchError, MaterialError
from users.services.material_service import MaterialService
from shared.dependencies.conn_db import get_connection_db
from shared.dependencies.redis import  get_lang_in_redis


router = APIRouter(prefix="/api/v1/materials",tags=["Materials"])

# get materials obj
def get_material_service_obj(connection = Depends(get_connection_db),lang = Depends(get_lang_in_redis)):
    return MaterialService(connection=connection,lang=lang)

# get all
@router.get("/")
@cache(expire=60*60*24,namespace="HOME_CACHE")
async def get_materials(material_service : MaterialService = Depends(get_material_service_obj),page : int = Query(default=1,ge=1),limit : int = Query(default=20,ge=5)):
    try :
       result = await  material_service.get_all_materials(page=page,limit=limit)
       return result

    except DbError as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"INTERNAL_SERVER_ERROR")

# filter
@router.get("/filter")
@cache(expire=60*60*24,namespace="FILTER_CACHE")
async def get_materials(material_service : MaterialService = Depends(get_material_service_obj), type : str = Query(...), semester :int = Query(...)):
    try :
       result = await  material_service.filter(type=type,semester=semester)
       return result
    except MaterialError as e :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except DbError as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"INTERNAL_SERVER_ERROR")



# search
@router.get("/search")
@cache(expire=60*30,namespace="SEARCH_CACHE")
async def search_by_subject_name(material_service : MaterialService = Depends(get_material_service_obj), subject_name : str = Query(...,min_length=1)):
    try :
       result = await  material_service.search_by_subject_name(subject_name=subject_name)
       return result
    except SearchError as e :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except DbError as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"INTERNAL_SERVER_ERROR")
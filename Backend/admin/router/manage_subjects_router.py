from fastapi import APIRouter,Depends,HTTPException,status,Form,File,UploadFile
from fastapi_cache.decorator import cache

from admin.services.manage_subjects_service import ManageSubjectService
from shared.dependencies.conn_db import get_connection_db
from shared.dependencies.redis import get_lang_in_redis
from shared.errors.errors import DbError

router = APIRouter(prefix="/api/v1/admin/subjects",tags=["Admin-Subjects"])

# get materials obj
def get_subjects_service_obj(connection = Depends(get_connection_db),lang = Depends(get_lang_in_redis)):
    return ManageSubjectService(connection=connection,lang=lang)

@router.get("/")
@cache(expire=60*60*24,namespace="SUBJECTS_CACHE")
async def get_all_subjects(subjects_services : ManageSubjectService = Depends(get_subjects_service_obj)):
    try:
        result =  await  subjects_services.get_all_subjects()
        return result
    except DbError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"INTERNAL_SERVER_ERROR")

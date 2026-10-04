import aiomysql
import os
from dotenv import load_dotenv

from shared.errors.errors import DbError, MaterialError
from admin.utils.boto3 import upload_to_s3

load_dotenv(override=True)
class Manage_MaterialService :
    def __init__(self, connection,lang):
        self.connection = connection
        self.lang = lang
    # check materials is exist
    async def check_materials_is_exist(self,id):
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                    """
                        SELECT id, `subject_id`, `semester`, `year_academic`, `type`, `session`, `file_url` 
                        FROM materials where id = %s
                    """,(id,))
            result = await cursor.fetchone()
            return result is not None

    # add materials
    async def add_material(self, subject_id,semester,year_academic,type,session,file):
        try :
            # upload to s3
            path = f"materials/semeter_{semester}/subject_{subject_id}/{type}/{file.filename}"
            file_url = f"{os.getenv("SUBDOMAIN")}/{path}"
            await upload_to_s3(file=file.file,file_name=path,redis=self.lang)

            # save in db
            async with self.connection.cursor() as cursor:
                await cursor.execute(
                """
                    INSERT INTO materials(`subject_id`,`semester`,`year_academic`,`type`,`session`,`file_url`)
                    VALUES(%s,%s,%s,%s,%s,%s)
                """,(subject_id,semester,year_academic,type,session,file_url))
            return {
                "success": True,
                "message" : self.lang["material"]["created"]
            }

        except aiomysql.Error:
            self.connection.rollback()
            raise DbError(self.lang["database"]["query_failed"])
# delete materials
    async def delete_materials(self,id : int) :
        if not await self.check_materials_is_exist(id) :
            raise MaterialError(self.lang["material"]["not_found"])

        try :
            async with self.connection.cursor() as cursor:
                await cursor.execute("""
                    DELETE FROM materials WHERE id = %s
                """,(id,))
            return {
                "success": True,
                "message" : self.lang["material"]["deleted"]
            }
        except aiomysql.Error:
            self.connection.rollback()
            raise DbError(self.lang["database"]["query_failed"])






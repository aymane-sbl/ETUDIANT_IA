import aiomysql

from shared.errors.errors import DbError


class ManageSubjectService:
    def __init__(self,connection,lang):
        self.connection = connection
        self.lang = lang

    # get all subjects
    async def get_all_subjects(self):
        try :
            async with self.connection.cursor() as cursor:
                await cursor.execute(
                    """
                        SELECT subjects.id , subjects.subject_name FROM subjects 
                        ORDER BY id ASC 
                    """)
                data =  await cursor.fetchall()
                return {
                    "success": True,
                    "data": data
                }
        except aiomysql.Error as e:
            raise DbError(self.lang["database"]["query_failed"])
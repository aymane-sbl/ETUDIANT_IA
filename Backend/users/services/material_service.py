from tarfile import FilterError
from unittest import result

import aiomysql
from math import ceil
from shared.errors.errors import DbError, SearchError, MaterialError


class MaterialService :
    def __init__(self,connection,lang):
        self.connection = connection
        self.lang = lang

    #get specific data
    async def __get_specific_data(self,column,value):
        allowed_columns = ["type","semester"]
        if column not in allowed_columns :
            raise DbError(self.lang["database"]["column_not_allowed"])
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                f"""
                SELECT materials.id, subjects.`subject_name`, `semester`, `year_academic`, `type`, `session`, `file_url`
                FROM materials
                INNER JOIN subjects ON subject_id = subjects.id
                WHERE materials.{column} = %s
                ORDER BY materials.id DESC

                """, (value,))
            data = await cursor.fetchall()
            return data


    # get All Materials
    async def get_all_materials(self,page : int,limit : int):
        try :
            async with self.connection.cursor() as cursor:
                offset = (page-1)*limit
                await cursor.execute(
                    """
                    SELECT materials.id,subjects.`subject_name`,`semester`,`year_academic`,`type`,`session`,`file_url` 
                    FROM materials INNER JOIN subjects ON subject_id = subjects.id
                    ORDER BY materials.id DESC 
                    LIMIT %s OFFSET %s
                    """,(limit,offset))
                data = await cursor.fetchall()
                # count
                await cursor.execute("""
                    SELECT COUNT(id) as count FROM materials
                """)
                count = await cursor.fetchone()
                return {
                    "success": True,
                    "pagination" : {
                        "current_page": page,
                        "limit": limit,
                        "total_pages": ceil(count["count"]/limit),
                        "total_items": count["count"]
                    },
                    "data": data
                }

        except aiomysql.Error as e:
            self.connection.rollback()
            raise DbError(self.lang["database"]["query_failed"])

    # filter
    async def filter(self,type,semester):
        try :
            async with self.connection.cursor() as cursor:
                await cursor.execute(""" 
                SELECT materials.id, subjects.`subject_name`, `semester`, `year_academic`, `type`, `session`, `file_url`
                FROM materials
                INNER JOIN subjects ON subject_id = subjects.id 
                WHERE type = %s AND semester = %s
                ORDER BY materials.id DESC
                """,(type,semester))

                data = await cursor.fetchall()
                if not data :
                    raise MaterialError(self.lang["material"]["not_found"])
                return {
                    "success": True,
                    "data": data
                }
        except aiomysql.Error as e:
            self.connection.rollback()
            raise DbError(self.lang["database"]["query_failed"])

#     search
    async def search_by_subject_name(self,subject_name : str):
        try :
            async with self.connection.cursor() as cursor:
                # query
                query = """
                            SELECT materials.id, subjects.`subject_name`, `semester`, `year_academic`, `type`, `session`, `file_url`
                            FROM materials
                            INNER JOIN subjects ON subject_id = subjects.id
                        """

                # check length of subject_name
                if len(subject_name) < 3:
                    where = "WHERE subjects.subject_name LIKE %s"
                    params = f"%{subject_name}%"
                else :
                    where = "WHERE MATCH(subjects.subject_name)AGAINST(%s)"
                    params = f"{subject_name}"

                full_query = f"{query} {where} ORDER BY materials.id DESC"
                await cursor.execute(full_query,(params,))
                data = await cursor.fetchall()

                # check data is empty
                if not data :
                    raise SearchError(self.lang["search"]["no_results"])

                return {
                    "success": True,
                    "data": data
                }
        except aiomysql.Error as e:
            self.connection.rollback()
            raise DbError(self.lang["database"]["query_failed"])

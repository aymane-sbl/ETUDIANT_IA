async def create_subject_table(connection):
    async with connection.cursor() as cursor:
        await cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    subject_name VARCHAR(255) UNIQUE NOT NULL,
                    FULLTEXT (subject_name)
                )
            """
        )
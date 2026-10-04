async def create_users_tables(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                `id` INT PRIMARY KEY AUTO_INCREMENT,
                `email` VARCHAR(255) UNIQUE NOT NULL,
                `password` VARCHAR(255) NOT NULL,
                `role` ENUM("admin","user") DEFAULT "user",
                `is_verified` BOOLEAN NOT NULL DEFAULT FALSE,
                `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
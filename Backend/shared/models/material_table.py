async def create_material_table(connection):
    async with connection.cursor() as cursor:
        await cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS materials(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    subject_id INT NOT NULL,
                    semester INT NOT NULL,
                    year_academic VARCHAR(200) NOT NULL,
                    type ENUM("COURS","TD","EXAM") DEFAULT "COURS" NOT NULL,
                    session ENUM("Normal","Rattrapage","none") DEFAULT "none" NOT NULL,
                    file_url TEXT NOT NULL,
                    FOREIGN KEY (subject_id) REFERENCES subjects(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )
            """)
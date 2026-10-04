from shared.models.material_table import create_material_table
from shared.models.subjects_table import create_subject_table
from shared.models.users_table import create_users_tables

async def init_tables(connection):
    await  create_subject_table(connection=connection)
    await create_material_table(connection=connection)
    await create_users_tables(connection=connection)
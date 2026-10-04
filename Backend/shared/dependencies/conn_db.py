from fastapi import Request
async def get_connection_db(request: Request):
    connection_pool = request.app.state.pool
    async with connection_pool.acquire() as connection:
        yield connection

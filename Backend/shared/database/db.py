import ssl
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv(override=True)

async def create_pool():
    # safe conn
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    pool = await  aiomysql.create_pool(
        host = os.getenv("HOST"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD"),
        db = os.getenv("DB"),
        ssl=ssl_ctx,
        minsize=5,
        maxsize=32,
        cursorclass = aiomysql.DictCursor,
        init_command =  'SET time_zone = "+00:00"',
        autocommit = True
    )
    return pool
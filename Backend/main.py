import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from  contextlib import asynccontextmanager
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

from shared.database.db import create_pool
from shared.database.redis import init_redis
from shared.dependencies.redis import set_lang_in_redis
from shared.models.init_tables import init_tables
from middleware.rate_limite import IpRateLimitMiddleware

from admin.router.manage_material_router import router as manage_material_router
from admin.router.manage_subjects_router import router as manage_subjects_router
from users.router.material_router import router as material_router
from auth.router.auth_router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # init db
    pool = await create_pool()
    app.state.pool = pool

    # init redis
    redis = init_redis()
    app.state.redis = redis
    redis_pool =  app.state.redis

    # init redis cache
    redis_cache = init_redis(decode_responses=False)
    FastAPICache.init(RedisBackend(redis_cache),prefix="ETUDIANT_IA")

    #init tables
    async with pool.acquire() as connection:
        await init_tables(connection=connection)

    # init lang
    await set_lang_in_redis(redis=redis_pool)

    yield
    pool.close()
    await pool.wait_closed()
app = FastAPI(lifespan=lifespan)
app.add_middleware(IpRateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","https://etudiant-ia.pages.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
            "welcome": "welcome to my api",
            "docs":"/docs",
            }

# router
# auth
app.include_router(auth_router)
# admin
app.include_router(manage_material_router)
app.include_router(manage_subjects_router)

# user
app.include_router(material_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


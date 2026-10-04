import json
from fastapi import Request,Depends

# connection
def get_redis_connection(request: Request):
    redis = request.app.state.redis
    yield redis
async def set_lang_in_redis(redis ,file_name="fr"):
    with open(fr"lang/{file_name}.json", "r") as f:
        data =  json.load(f)
    await redis.set("ETUDIANT_IA:lang", json.dumps(data))


async def get_lang_in_redis(redis = Depends(get_redis_connection)):
    get_lang =await redis.get("ETUDIANT_IA:lang")
    return  json.loads(get_lang)

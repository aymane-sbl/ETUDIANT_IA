from shared.errors.errors import TooManyAttempts


async def check_email_rate_limit(email, redis, lang: dict):
    redis_key = f"ETUDIANT_IA:auth_limit:{email}"
    attempts = await redis.incr(redis_key)
    if attempts == 1:
        await redis.expire(redis_key, 5*60)
    if attempts > 5:
        raise TooManyAttempts(lang["auth"]["too_many_attempts"])
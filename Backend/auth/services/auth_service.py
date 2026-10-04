import aiomysql
from datetime import datetime,timezone,timedelta

from auth.utils.email_rate_limit import check_email_rate_limit
from auth.utils.securite import hash_password, verify_password, encode_token
from shared.errors.errors import DbError, AuthError


class AuthService :
    def __init__(self,connection,lang,redis):
        self.connection = connection
        self.lang = lang
        self.redis = redis
    # check email is exist
    async def __check_email_is_exist(self,email):
        async with self.connection.cursor() as cursor:
            await cursor.execute("SELECT email FROM users WHERE email = %s",(email,))
            data = await cursor.fetchone()
            return data is not None
    # register
    async def register(self,email,password):
        try :
            await check_email_rate_limit(email=email,lang=self.lang,redis = self.redis)
            # check email
            if await self.__check_email_is_exist(email=email) :
                raise AuthError(self.lang["auth"]["email_exist"])

            async with self.connection.cursor() as cursor:
                hashed_password = hash_password(password=password)
                date_now = datetime.now(timezone.utc)
                await cursor.execute(
                    """
                        INSERT INTO users (email,password,created_at) VALUES (%s,%s,%s)
                     """,(email,hashed_password,date_now))
                return {
                    "success": True,
                    "message" : self.lang["auth"]["registration_success"]
                }
        except aiomysql.Error as e:
            self.connection.rollback()
            raise DbError(self.lang["database"]["query_failed"])

    #login
    async def login(self,email,password):
        try :
            await check_email_rate_limit(email=email, lang=self.lang, redis=self.redis)
            # check email
            if not await  self.__check_email_is_exist(email=email):
                raise AuthError(self.lang["auth"]["email_not_found"])
            # verify password
            async with self.connection.cursor() as cursor:
                await cursor.execute("""SELECT email, password,role
                                        FROM users
                                        WHERE email = %s""", (email,))
                data = await cursor.fetchone()
                hashed_password = data["password"]
                verify_password(password=password, hashed_password=hashed_password, lang=self.lang)

                # create token
                payload = {
                    "sub" : email,
                    "role":data["role"],
                    "exp" : datetime.now(timezone.utc) + timedelta(days=30),
                }

                token = encode_token(payload=payload)
                return {
                    "success": True,
                    "message": self.lang["auth"]["login_success"],
                    "role" : data["role"],
                    "access_token": token,
                    "token_type": "bearer",
                }
        except aiomysql.Error as e:
            self.connection.rollback()
            raise DbError(self.lang["database"]["query_failed"])

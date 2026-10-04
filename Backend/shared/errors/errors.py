# db error
class DbError(Exception):
    pass

# s3 error
class S3UploadError(Exception):
    pass

# search error
class SearchError(Exception):
    pass

# Auth error
class AuthError(Exception):
    pass

class TooManyAttempts(Exception):
    pass

class MaterialError(Exception):
    pass

class UnauthorizedError(Exception):
    pass
from shared.errors.errors import UnauthorizedError

def check_is_admin(role):
    if role != "admin" :
        raise UnauthorizedError("Unauthorized")

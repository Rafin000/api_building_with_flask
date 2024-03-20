from src.api.users.crud import get_user_by_username

def verify_user(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None
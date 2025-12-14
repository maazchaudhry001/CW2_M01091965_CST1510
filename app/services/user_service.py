from app.data.users import find_user, insert_user, get_user_by_username
import bcrypt
def register_user(username, password):
    if get_user_by_username(username):
        return False
    insert_user(username, password)
    return True

def authenticate(username, password):
    user = get_user_by_username(username)
    if not user:
        return False

    return bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode("utf-8"))
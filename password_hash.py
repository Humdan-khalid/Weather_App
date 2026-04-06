from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10
)

def create_hash_password(password: str):
    hashed_password = pwd_context.hash(password)

    if password is None:
        return ValueError("Password is None")
    
    return hashed_password

def verify_hash_password(user_password: str, hash_password: str):
    if user_password is None:
        return ValueError("user password is None!")
    password_verification = pwd_context.verify(user_password, hash_password)
    return password_verification


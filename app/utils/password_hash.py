from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10
)

def create_hash_password(password: str):
    if password is None:
        raise ValueError("password is None!")
    
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_hash_password(user_password: str, hash_password: str):
    password_verification = pwd_context.verify(user_password, hash_password)
    return password_verification
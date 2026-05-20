from passlib.context import CryptContext


# Password hashing context using Argon2 algorithm
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# Utility function to hash a password
def hash_password(password: str) -> str:
    """Hash the password using Argon2 algorithm."""
    return pwd_context.hash(password)


# Utility function to verify a password against its hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
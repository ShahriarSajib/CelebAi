import bcrypt

def hash_password(password: str) -> str:
    # Convert password string to bytes
    pwd_bytes = password.encode('utf-8')
    # Generate a secure salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Return the decoded string version to save into PostgreSQL
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert both strings back to bytes for secure comparison
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

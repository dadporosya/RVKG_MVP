import bcrypt

SALT = bcrypt.gensalt()

def hash(s:str) -> str:
    return bcrypt.hashpw(s.encode(), SALT).decode()

def compareHashedAndStr(s:str, hashed:str) -> bool:
    return  bcrypt.checkpw(s.encode(), hashed.encode())

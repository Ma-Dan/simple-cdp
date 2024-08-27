import bcrypt


def hash_pwd(pwd: str):
    salt = bcrypt.gensalt(10)
    pwd = pwd.encode('utf-8')
    return bcrypt.hashpw(pwd, salt).decode('utf-8')


def compare_pwd(pwd: str, pwd_hash: str):
    pwd = pwd.encode('utf-8')
    pwd_hash = pwd_hash.encode('utf-8')
    return bcrypt.checkpw(pwd, pwd_hash)

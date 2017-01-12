# Hashing/Salting
import hashlib, uuid

def generateHash(password, salt):
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

def generateSalt():
    return uuid.uuid4().hex

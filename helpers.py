from passlib.context import CryptContext
from database import SessonLocal

#hashing user password 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


#get database else or close the connection
def get_db():
    db = SessonLocal()
    try:
        yield db
    finally:
        db.close()
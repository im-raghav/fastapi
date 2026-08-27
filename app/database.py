from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
# DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi"
# DATABASE_URL = "postgresql://neondb_owner:npg_sJUVpt2MYRX7@ep-withered-glitter-azup17cx-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database connected succesfully")
#         break
#     except Exception as error:
#         print("Database connection failed with error: ", error)
#         time.sleep(3)



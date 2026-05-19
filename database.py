# Importing create_engine to establish a connection to the database
from sqlalchemy import create_engine    

# Importing sessionmaker to create a session for database operations
from sqlalchemy.orm import sessionmaker

# Importing declarative_base to create the base class for ORM models
from sqlalchemy.ext.declarative import declarative_base


# Database connection 
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Santhu@7022'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DB = 'fastapi_db'

# Database URL
# DATABASE_URL = "mysql+pymysql://root:password123@localhost:3306/my_fastapi_db"
DATABASE_URL = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'


# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)


# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a base class for our ORM models
Base = declarative_base()
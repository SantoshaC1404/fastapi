# Importing create_engine to establish a connection to the database
from sqlalchemy import create_engine

# Importing sessionmaker to create a session for database operations
from sqlalchemy.orm import sessionmaker

# Importing declarative_base to create the base class for ORM models
from sqlalchemy.ext.declarative import declarative_base

from urllib.parse import quote_plus
import os


# Database connection 
MYSQL_USER = os.getenv('MYSQL_USER', 'root')  # Default to 'root' if not set
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Santhu@7022')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')  # Default to 'db' if not set (matches the service name in docker-compose)
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_DB = os.getenv('MYSQL_DB', 'fastapi_db')

# Database URL
# DATABASE_URL = "mysql+pymysql://root:password123@localhost:3306/my_fastapi_db"
encoded_user = quote_plus(MYSQL_USER)
encoded_password = quote_plus(MYSQL_PASSWORD)
DATABASE_URL = (
    f'mysql+pymysql://{encoded_user}:{encoded_password}'
    f'@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
)


# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Enable SQL query logging for debugging
    pool_pre_ping=True  # This option checks if the connection is alive before using it, which can help prevent "MySQL server has gone away" errors      
)


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
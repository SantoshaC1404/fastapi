from database import Base
from sqlalchemy import Column, Integer, VARCHAR

# Defining the User model which inherits from the Base class
class Books(Base):
    __tablename__ = 'books' # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    title = Column(VARCHAR(255))    # title column to store the title of the book
    author = Column(VARCHAR(255))   # author column to store the name of the author

    
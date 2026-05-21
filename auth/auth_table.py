from auth.auth_database import Base, engine
from auth import models


# Creating the tables in the database based on the defined models
Base.metadata.create_all(bind=engine)
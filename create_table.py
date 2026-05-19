from database import Base, engine
import model


# Creating the tables in the database based on the defined models
Base.metadata.create_all(bind=engine)
from app.database.database import engine, Base
from app.database import models


Base.metadata.create_all(bind=engine)

print("Database created successfully!")
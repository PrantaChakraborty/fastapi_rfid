from src.database import engine
from src.auth import models

print("creating db ...")
try:
    models.Base.metadata.create_all(bind = engine)
except Exception as e:
    print(e)

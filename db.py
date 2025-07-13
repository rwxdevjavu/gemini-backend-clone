from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

session = sessionmaker(bind=engine,autoflush=True)

db_session = session()

BASE = declarative_base();

# BASE.metadata.drop_all(bind=engine)
# BASE.metadata.create_all(bind=engine)


# try:
#     connection = engine.connect()
#     print('connected')
# except Exception as e:
#     print("err",e)
# finally:
#     connection.close()

# Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:secret@localhost:3306/pyhton-de"

engine = create_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=10)

# Use declarative_base() instead of DeclarativeBase
Base = declarative_base()

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

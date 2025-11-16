from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

data_base_url = "mysql+pymysql://root:secret@localhost:3306/pyhton-de"

engine = create_engine(data_base_url, echo=True, pool_size=5, max_overflow=10)


Base = declarative_base()


Session = sessionmaker(bind=engine)

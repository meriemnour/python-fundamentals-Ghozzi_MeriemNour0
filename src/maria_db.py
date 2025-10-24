from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:secret@localhost:3306/pyhton-de"

engine = create_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=10)

with engine.connect() as connection:
    with connection.begin():
        sql = text("INSERT INTO users(username, email) VALUES(:username, :email);")
        params = {"username": "mohamed", "email": "mohamed@gmail.com"}
        result = connection.execute(sql, params)

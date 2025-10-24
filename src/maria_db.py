from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, String, create_engine, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = "mysql+pymysql://root:secret@localhost:3306/pyhton-de"

engine = create_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=10)

# metadata= MetaData()

# users_table = Table(
#   "users",
#   metadata,
#   Column("id", Integer, primary_key=True),
#   Column("username", String(50), nullable=False, unique=True),
#   Column("email", String(100), nullable=False),
#   Column("created_at", DateTime, default=datetime.utcnow),
# )

# comments_table=Table(
#   "comments",
#   metadata,
#   Column("id", Integer, primary_key=True),
#   Column("user_id", Integer, nullable=False),
#   Column("comment", String(255), nullable=False),
#   Column("created_at", DateTime, default=datetime.utcnow),
# )


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

with Session() as session:
    query = select(User).where(User.username == "mimou")
    result = session.execute(query)
    user = result.scalars().one()

    print(f"Type: {type(user)}")
    print(f"User ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Created at: {user.created_at}")

    print("***")
    query2 = select(User)
    result2 = session.execute(query2)
    user2 = result2.scalars().all()
    for use_r in user2:
        print(use_r.username, use_r.email)
    print("***")
    for use_r in user2:
        print(use_r.username, use_r.email)

    # update column value in table (email)
    query3 = select(User).where(User.username == "mimou")
    result = session.execute(query3)
    user3 = result.scalars().one()
    print(f"Before update - Email: {user3.email}")
    user3.email = "mohamed@yahoo.tn"
    session.commit()
    print("******")


def retrieve_all_users() -> List[User]:
    with Session() as session:
        query = select(User)
        result = session.execute(query)
        users = result.scalars().all()
        return users


def retrieve_user_by_username(username: str) -> Optional[User]:
    with Session() as session:
        query = select(User).where(User.username == username)
        result = session.execute(query)
        user = result.scalars().first()
        return user


def insert_user(username: str, email: str) -> None:
    with Session() as session:
        stmt = insert(User).values(username=username, email=email)
        session.execute(stmt)
        session.commit()
        print(username, email)


def update_user(user_id: int, username: str = None, email: str = None) -> None:
    with Session() as session:
        user = session.get(User, user_id)
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            session.commit()
            print(f" {user_id} success")
        else:
            print(f"{user_id} not found")


if __name__ == "__main__":
    print(" All Users ")
    all_users = retrieve_all_users()
    for user in all_users:
        print(user.username, user.email)
    print(" example username from table : mimou")
    user = retrieve_user_by_username("mimou")
    if user:
        print(user.username, user.email)
    else:
        print("Not found")

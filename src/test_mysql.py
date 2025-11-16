# test_mysql.py
from src.storage.relational_db import engine

try:
    with engine.connect() as conn:
        print("✅ MySQL connection successful!")
        # Check if tables exist
        from sqlalchemy import inspect

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("Tables in database:", tables)

        if not tables:
            print("No tables found. Creating tables...")
            from src.storage.relational_db import Base

            Base.metadata.create_all(engine)
            tables = inspector.get_table_names()
            print("Tables after creation:", tables)

except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
    print("This usually means:")
    print("1. MySQL service is not running")
    print("2. Wrong credentials in connection string")
    print("3. Database 'pyhton-de' doesn't exist")

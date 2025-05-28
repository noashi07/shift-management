import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/shift"

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)


def init_db():
    """This is used to initialize the tables in the db on startup"""
    Base.metadata.create_all(engine)
    print("Database connected and tables created.")


def get_session():
    """"This is used to return the session (actual connection) to the db.  """
    return Session()

import subprocess
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"shift_backup_{timestamp}.sql"

    # Set password in environment variable
    env = os.environ.copy()
    env["PGPASSWORD"] = "postgres"  # ⚠️ Don't hardcode passwords in production

    try:
        subprocess.run([
            "pg_dump",
            "-U", "postgres",
            "-F", "c",  # custom format
            "-f", backup_file,
            "shift"
        ], check=True, env=env)
        print(f"✅ Backup successful: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed: {e}")
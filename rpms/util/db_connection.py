import os
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": os.getenv("RPMS_DB_HOST", "localhost"),
    "port": int(os.getenv("RPMS_DB_PORT", "3306")),
    "user": os.getenv("RPMS_DB_USER", "root"),
    "password": os.getenv("RPMS_DB_PASSWORD", ""),  # Change or set RPMS_DB_PASSWORD as per your MySQL setup
    "database": os.getenv("RPMS_DB_NAME", "recruitment_portal"),
    "use_pure": True,
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as exc:
        raise RuntimeError(f"Database connection failed: {exc}") from exc

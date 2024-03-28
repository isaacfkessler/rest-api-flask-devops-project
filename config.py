import os


class DevConfig:
    MONGODB_SETTINGS = [
        {
            "db": os.getenv("MONGODB_DB"),
            "host": os.getenv("MONGODB_HOST"),
            "port": 27017,
            "username": os.getenv("MONGODB_USERNAME"),
            "password": os.getenv("MONGODB_PASSWORD"),
        }
    ]


class ProdConfig:
    MONGODB_USER = os.getenv("MONGODB_USER")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
    MONGODB_HOST = os.getenv("MONGODB_HOST")
    MONGODB_DB = os.getenv("MONGODB_DB")

    URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}/{MONGODB_DB}"
    MONGODB_SETTINGS = {"host": URI}


class MockConfig:
    MONGODB_SETTINGS = [
        {
            "db": "users",
            "host": "mongomock://localhost",
        }
    ]

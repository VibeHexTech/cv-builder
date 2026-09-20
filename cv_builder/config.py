import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://cvbuilder:cvbuilder@localhost/cvbuilder",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

from sqlalchemy import inspect, text

from .extensions import db


LOCK_COLUMN = "locked"
DELETED_AT_COLUMN = "deleted_at"


def initialize_database(app):
    with app.app_context():
        db.create_all()
        columns = {column["name"] for column in inspect(db.engine).get_columns("cv_entries")}
        if LOCK_COLUMN not in columns:
            db.session.execute(
                text("ALTER TABLE cv_entries ADD COLUMN locked BOOLEAN NOT NULL DEFAULT FALSE")
            )
            db.session.commit()
            columns.add(LOCK_COLUMN)
        if DELETED_AT_COLUMN not in columns:
            db.session.execute(
                text("ALTER TABLE cv_entries ADD COLUMN deleted_at TIMESTAMP NULL")
            )
            db.session.commit()

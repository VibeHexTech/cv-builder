from .extensions import db


class CvEntry(db.Model):
    __tablename__ = "cv_entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    opgave = db.Column(db.Text, nullable=False)
    rolle = db.Column(db.String(200), nullable=False)
    resultat = db.Column(db.Text, nullable=False)
    locked = db.Column(db.Boolean, nullable=False, default=False, server_default="false")
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "opgave": self.opgave,
            "rolle": self.rolle,
            "resultat": self.resultat,
            "locked": self.locked,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

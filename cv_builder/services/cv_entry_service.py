from datetime import datetime, timezone


REQUIRED_FIELDS = ("title", "opgave", "rolle", "resultat")


class CvEntryService:
    def __init__(self, session, entry_model):
        self.session = session
        self.entry_model = entry_model

    def list_entries(self, include_deleted=False):
        query = self.entry_model.query
        if not include_deleted:
            query = query.filter(self.entry_model.deleted_at.is_(None))
        return query.order_by(self.entry_model.id).all()

    def list_deleted_entries(self):
        return self.entry_model.query.filter(
            self.entry_model.deleted_at.is_not(None)
        ).order_by(self.entry_model.id).all()

    def get_entry(self, item_id):
        return self.session.get(self.entry_model, item_id)

    def create_entry(self, payload):
        self._validate_payload(payload)
        entry = self.entry_model(**{field: payload[field] for field in REQUIRED_FIELDS})
        self.session.add(entry)
        self.session.commit()
        return entry

    def update_entry(self, item_id, payload):
        entry = self.get_entry(item_id)
        if not entry:
            return None

        for field in REQUIRED_FIELDS:
            if field in payload and payload[field]:
                setattr(entry, field, payload[field])
        if "locked" in payload:
            entry.locked = bool(payload["locked"])

        self.session.commit()
        return entry

    def delete_entry(self, item_id):
        entry = self.get_entry(item_id)
        if not entry:
            return "not_found"
        if entry.locked:
            return "locked"

        entry.deleted_at = datetime.now(timezone.utc)
        self.session.commit()
        return "deleted"

    def recover_entry(self, item_id):
        entry = self.get_entry(item_id)
        if not entry:
            return "not_found"
        if entry.deleted_at is None:
            return "active"

        entry.deleted_at = None
        self.session.commit()
        return "recovered"

    def save_rows(self, rows):
        if not isinstance(rows, list) or not rows:
            raise ValueError("No rows supplied")

        entries = []
        for row in rows:
            if not all(str(row.get(field, "")).strip() for field in REQUIRED_FIELDS):
                continue

            entry = self.entry_model(
                **{field: str(row[field]).strip() for field in REQUIRED_FIELDS}
            )
            self.session.add(entry)
            entries.append(entry)

        if not entries:
            raise ValueError("No valid rows were saved")

        self.session.commit()
        return entries

    @staticmethod
    def _validate_payload(payload):
        for field in REQUIRED_FIELDS:
            if not payload.get(field):
                raise ValueError(f"Missing required field: {field}")

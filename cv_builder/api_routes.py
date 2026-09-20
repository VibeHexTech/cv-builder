from flask_restx import Api, Namespace, Resource, fields

from .models import CvEntry
from .extensions import db
from .services.cv_entry_service import CvEntryService


api = Api(
    title="CV Builder API",
    version="1.0",
    description="REST API for managing CV entries with PostgreSQL.",
    doc="/docs",
)
entries_namespace = Namespace("entries", path="/api")
api.add_namespace(entries_namespace)
entry_service = CvEntryService(db.session, CvEntry)

cv_entry_model = entries_namespace.model(
    "CvEntry",
    {
        "title": fields.String(required=True, description="Title"),
        "opgave": fields.String(required=True, description="Opgave"),
        "rolle": fields.String(required=True, description="Rolle"),
        "resultat": fields.String(required=True, description="Resultat"),
        "locked": fields.Boolean(required=False, description="Prevent deletion"),
    },
)


@entries_namespace.route("/items")
class CvEntryList(Resource):
    @entries_namespace.doc("list_cv_entries")
    def get(self):
        return [entry.to_dict() for entry in entry_service.list_entries()]


@entries_namespace.route("/items/all")
class CvEntryAllList(Resource):
    @entries_namespace.doc("list_all_cv_entries")
    def get(self):
        items = entry_service.list_entries()
        return {"count": len(items), "items": [entry.to_dict() for entry in items]}

    @entries_namespace.doc("create_cv_entry")
    @entries_namespace.expect(cv_entry_model, validate=True)
    def post(self):
        try:
            entry = entry_service.create_entry(entries_namespace.payload or {})
        except ValueError as exc:
            return {"message": str(exc)}, 400
        return entry.to_dict(), 201


@entries_namespace.route("/items/deleted")
class CvEntryDeletedList(Resource):
    @entries_namespace.doc("list_deleted_cv_entries")
    def get(self):
        items = entry_service.list_deleted_entries()
        return {"count": len(items), "items": [entry.to_dict() for entry in items]}


@entries_namespace.route("/items/<int:item_id>")
class CvEntryDetail(Resource):
    @entries_namespace.doc("get_cv_entry")
    def get(self, item_id):
        entry = entry_service.get_entry(item_id)
        if not entry:
            return {"message": "Item not found"}, 404
        return entry.to_dict()

    @entries_namespace.doc("update_cv_entry")
    @entries_namespace.expect(cv_entry_model, validate=False)
    def put(self, item_id):
        entry = entry_service.update_entry(item_id, entries_namespace.payload or {})
        if not entry:
            return {"message": "Item not found"}, 404
        return entry.to_dict()

    @entries_namespace.doc("delete_cv_entry")
    def delete(self, item_id):
        result = entry_service.delete_entry(item_id)
        if result == "not_found":
            return {"message": "Item not found"}, 404
        if result == "locked":
            return {"message": "Locked entries cannot be deleted"}, 409
        return {"message": "Item moved to deleted entries"}, 200


@entries_namespace.route("/items/<int:item_id>/recover")
class CvEntryRecover(Resource):
    @entries_namespace.doc("recover_cv_entry")
    def post(self, item_id):
        result = entry_service.recover_entry(item_id)
        if result == "not_found":
            return {"message": "Item not found"}, 404
        if result == "active":
            return {"message": "Item is already active"}, 409
        return {"message": "Item recovered"}, 200

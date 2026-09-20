from flask import Blueprint, jsonify, request

from .services.cv_entry_service import CvEntryService
from .services.docx_parser import extract_docx_rows


docx_bp = Blueprint("docx", __name__)


def get_entry_service():
    from .extensions import db
    from .models import CvEntry

    return CvEntryService(db.session, CvEntry)


@docx_bp.post("/api/docx/import")
def import_docx():
    uploaded = request.files.get("file")
    if not uploaded:
        return jsonify({"message": "No file uploaded"}), 400

    if not (uploaded.filename or "").lower().endswith(".docx"):
        return jsonify({"message": "Only .docx files are supported"}), 400

    try:
        rows = extract_docx_rows(uploaded)
    except Exception as exc:  # pragma: no cover - defensive error for uploaded file
        return jsonify({"message": f"Could not read DOCX file: {exc}"}), 400

    if not rows:
        return jsonify({"message": "No matching table rows with Title/Opgave/Rolle/Resultat were found."}), 400

    return jsonify({"rows": rows, "count": len(rows)})


@docx_bp.post("/api/docx/save")
def save_docx_entries():
    data = request.get_json(silent=True) or {}
    try:
        saved = get_entry_service().save_rows(data.get("rows") or [])
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400

    return jsonify({"saved": len(saved), "items": [entry.to_dict() for entry in saved]})

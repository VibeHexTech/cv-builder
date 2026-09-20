from flask import Blueprint, render_template


web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def index():
    return render_template("index.html")


@web_bp.get("/file-upload")
def file_upload():
    return render_template("file_upload.html")


@web_bp.get("/manual-entry")
def manual_entry():
    return render_template("manual_entry.html")


@web_bp.get("/new-entry")
def new_entry():
    return render_template("new_entry.html")


@web_bp.get("/deleted-entries")
def deleted_entries():
    return render_template("deleted_entries.html")

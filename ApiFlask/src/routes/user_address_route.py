from flask import Blueprint, jsonify, request, current_app
from dependency_injector.providers import Provider

from container import Container
from src.exceptions.import_exceptions import (
    InvalidFileType,
    MissMatchColumnsError,
    NoColumnsError,
    NoFileProvided,
)

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/import-address", methods=["POST"])
def import_user_address():

    if request.content_type and not request.content_type.startswith(
        "multipart/form-data"
    ):
        return jsonify({"error": "Invalid content type"}), 400

    file = request.files.get("file", None)
    container: Container = current_app.container  # type: ignore
    controller = container.user_address_controller()

    try:
        result = controller.import_user_address(file)
    except (
        NoFileProvided,
        InvalidFileType,
        NoColumnsError,
        MissMatchColumnsError,
    ) as e:
        return jsonify({"error": str(e)}), 400

    return result or jsonify({"sim": "sim"})

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
    # TODO: Create an adapter to UserAddressSchema from file
    try:
        rows_with_errors = controller.import_user_address(file)
    except (
        NoFileProvided,
        InvalidFileType,
        NoColumnsError,
        MissMatchColumnsError,
    ) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"error": "Unexpected error. Try again later or contact support."}),
            500,
        )

    if rows_with_errors:
        return (
            jsonify(
                {
                    "message": "User addresses partial imported",
                    "rows_with_errors": rows_with_errors,
                }
            ),
            207,
        )
    return jsonify({"message": "User addresses imported successfully"}), 201

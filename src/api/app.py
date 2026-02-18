"""Flask API backend for serving scraped data."""

import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from azure_storage.repository import AzureBlobRepository
from utils.logger import Logger

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

logger = Logger()

# Initialize repository
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
repository = AzureBlobRepository(connection_string)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "API is running"}), 200


@app.route("/api/data/latest", methods=["GET"])
def get_latest_data():
    """Get the latest scraped data."""
    try:
        data = repository.get_latest_data()

        if data is None:
            return (
                jsonify(
                    {
                        "error": "No data available",
                        "message": "No scraped data found in blob storage",
                    }
                ),
                404,
            )

        return jsonify(data), 200

    except Exception as e:
        logger.log_error(f"Error retrieving latest data: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route("/api/data/blobs", methods=["GET"])
def list_blobs():
    """List all available data blobs."""
    try:
        blobs = repository.get_all_blobs()

        return jsonify({"count": len(blobs), "blobs": blobs}), 200

    except Exception as e:
        logger.log_error(f"Error listing blobs: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route("/api/data/<blob_name>", methods=["GET"])
def get_data_by_blob(blob_name):
    """Get data by specific blob name."""
    try:
        data = repository.get_data_by_blob_name(blob_name)

        if data is None:
            return (
                jsonify(
                    {
                        "error": "Blob not found",
                        "message": f"No data found for blob: {blob_name}",
                    }
                ),
                404,
            )

        return jsonify(data), 200

    except Exception as e:
        logger.log_error(f"Error retrieving blob {blob_name}: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def serve_frontend():
    """Serve the main frontend page."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>", methods=["GET"])
def serve_static(path):
    """Serve static files."""
    if path.startswith("api/"):
        return jsonify({"error": "Not found"}), 404

    return send_from_directory(app.static_folder, path)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return (
        jsonify(
            {"error": "Not found", "message": "The requested resource was not found"}
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.log_error(f"Internal server error: {error}")
    return (
        jsonify(
            {
                "error": "Internal server error",
                "message": "An unexpected error occurred",
            }
        ),
        500,
    )


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    port = int(os.getenv("PORT", 5000))

    logger.log_info(f"Starting Flask API server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)

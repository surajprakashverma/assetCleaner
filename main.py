from io import BytesIO
import inspect
import re

from flask import Flask, request, send_file, render_template

from EventCleanUp import eventCleanUp
from VFSCleanUp import vfsCleanUp


app = Flask(__name__)


def validate_vfs_paths(vfs_paths):
    paths = [
        path.strip()
        for path in vfs_paths.splitlines()
        if path.strip()
    ]

    if not paths:
        return False, (
            "VFS paths are required. "
            "Please enter at least one VFS path before submitting."
        )

    invalid_paths = []

    vfs_path_pattern = re.compile(
        r"^/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/?$"
    )

    for path in paths:
        if not vfs_path_pattern.match(path):
            invalid_paths.append(path)

    if invalid_paths:
        error_message = (
            "Invalid VFS path format found. "
            "Please enter one valid VFS path per line. "
            "Each path must start with '/' and should not contain spaces, double slashes, "
            "or unsupported special characters.\n\n"
            "Invalid path(s):\n"
            + "\n".join(invalid_paths)
            + "\n\nCorrect examples:\n"
            "/CS/CS_AT_SPV/Inbound/\n"
            "/CS/CS_AT_SPV/Outbound/\n"
            "/RPI/BUK/RT/MDM/Customer\n"
            "/RPI/BUK/RT/MDM/Customer/"
        )

        return False, error_message

    return True, paths


def process_uploaded_file(asset_type):
    try:
        uploaded_file = request.files.get("file")

        if not uploaded_file:
            return render_template(
                "error.html",
                error_message=(
                    "No file was uploaded. "
                    "Please select a valid XML file and try again."
                )
            )

        if uploaded_file.filename == "":
            return render_template(
                "error.html",
                error_message=(
                    "No file was selected. "
                    "Please choose an XML file before submitting."
                )
            )

        if not uploaded_file.filename.lower().endswith(".xml"):
            return render_template(
                "error.html",
                error_message=(
                    "Only XML files are supported. "
                    "Please upload a valid .xml file."
                )
            )

        xml_bytes = uploaded_file.read()

        if not xml_bytes:
            return render_template(
                "error.html",
                error_message=(
                    "The uploaded XML file is empty. "
                    "Please upload a valid Software AG export XML file."
                )
            )

        if asset_type == "event":
            tree = eventCleanUp(
                BytesIO(xml_bytes)
            )

        elif asset_type == "vfs":
            vfs_paths = request.form.get(
                "vfs_paths",
                ""
            ).strip()

            is_valid, validation_result = validate_vfs_paths(vfs_paths)

            if not is_valid:
                return render_template(
                    "error.html",
                    error_message=validation_result
                )

            vfs_function_parameters = inspect.signature(
                vfsCleanUp
            ).parameters

            if len(vfs_function_parameters) == 1:
                tree = vfsCleanUp(
                    BytesIO(xml_bytes)
                )
            else:
                tree = vfsCleanUp(
                    BytesIO(xml_bytes),
                    vfs_paths
                )

        else:
            return render_template(
                "error.html",
                error_message=(
                    "Invalid cleanup type selected. "
                    "Please go back to home and choose Event Cleanup or VFS Cleanup."
                )
            )

        output = BytesIO()

        tree.write(
            output,
            pretty_print=True
        )

        output.seek(0)

        return send_file(
            output,
            mimetype="application/xml",
            as_attachment=True,
            download_name=uploaded_file.filename
        )

    except Exception as e:
        error_text = str(e)

        if "takes 1 positional argument but 2 were given" in error_text:
            error_text = (
                "VFS Cleanup configuration mismatch. "
                "The VFS cleanup function argument count does not match the application input. "
                "Please check VFSCleanUp.py function definition."
            )

        elif "XMLSyntaxError" in error_text:
            error_text = (
                "Invalid XML format. "
                "Please upload a valid Software AG MFT export XML file."
            )

        elif "Start tag expected" in error_text:
            error_text = (
                "The uploaded file does not look like a valid XML file. "
                "Please verify the file content and upload again."
            )

        elif "Permission denied" in error_text:
            error_text = (
                "Permission issue occurred while processing the file. "
                "Please close the file if it is open somewhere and try again."
            )

        elif "NoneType" in error_text:
            error_text = (
                "Required XML data was not found in the uploaded file. "
                "Please verify that the uploaded file is a valid Software AG export."
            )

        return render_template(
            "error.html",
            error_message=error_text
        )


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/event", methods=["GET", "POST"])
def event_page():
    if request.method == "POST":
        return process_uploaded_file("event")

    return render_template("event.html")


@app.route("/vfs", methods=["GET", "POST"])
def vfs_page():
    if request.method == "POST":
        return process_uploaded_file("vfs")

    return render_template("vfs.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        error_message=(
            "The page you are looking for was not found. "
            "Please go back to home and select a valid option."
        )
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "error.html",
        error_message=(
            "Internal server error occurred. "
            "Please try again or contact the application administrator."
        )
    ), 500


if __name__ == "__main__":
    app.run(debug=True)

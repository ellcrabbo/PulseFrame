import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uuid

from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

from visualiser import generate_waveform_plot  # must exist in same project folder

app = Flask(__name__)
UPLOAD_DIR = os.path.join("static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"wav"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    waveform_url = None
    spectrum_url = None
    audio_url = None
    error_message = None

    if request.method == "POST":
        file = request.files.get("audio_file")
        if not file or not file.filename:
            error_message = "Please choose a WAV file to upload."
        elif not allowed_file(file.filename):
            error_message = "Only WAV files with a .wav extension are supported."
        else:
            original_name = secure_filename(file.filename)
            name, ext = os.path.splitext(original_name)
            unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_name)
            file.save(file_path)

            waveform_name, spectrum_name = generate_waveform_plot(file_path, UPLOAD_DIR)

            audio_url = url_for("static", filename=f"uploads/{unique_name}")
            waveform_url = url_for("static", filename=f"uploads/{waveform_name}")
            spectrum_url = url_for("static", filename=f"uploads/{spectrum_name}")

    return render_template(
        "index.html",
        waveform_url=waveform_url,
        spectrum_url=spectrum_url,
        audio_url=audio_url,
        error_message=error_message,
    )


if __name__ == "__main__":
    app.run(debug=True)

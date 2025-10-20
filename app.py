import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request
from visualiser import generate_waveform_plot  # must exist in same project folder

app = Flask(__name__)
UPLOAD_DIR = os.path.join("static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    waveform_url = None
    spectrum_url = None

    if request.method == "POST":
        file = request.files.get("audio_file")
        if file and file.filename.endswith(".wav"):
            path = os.path.join(UPLOAD_DIR, file.filename)
            file.save(path)

            # generate_waveform_plot should return two file paths:
            # waveform_path, spectrum_path
            waveform_path, spectrum_path = generate_waveform_plot(path)

            # Build URLs for browser to access via static/
            waveform_url = f"/{waveform_path.replace(os.sep, '/')}"
            spectrum_url = f"/{spectrum_path.replace(os.sep, '/')}"

    return render_template("index.html", waveform_url=waveform_url, spectrum_url=spectrum_url)


if __name__ == "__main__":
    app.run(debug=True)
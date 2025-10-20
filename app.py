from flask import Flask, render_template, request, send_file
import os
from utils.audio_tools import read_wave
from utils.visualiser import render_waveform

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    image_path = None
    if request.method == "POST":
        file = request.files.get("audio")
        if file and file.filename.endswith(".wav"):
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            samples, samplerate = read_wave(path)
            image_path = render_waveform(samples, samplerate, file.filename)
    return render_template("index.html", image_path=image_path)

@app.route("/waveform/<filename>")
def waveform(filename):
    return send_file(os.path.join("outputs", filename), mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
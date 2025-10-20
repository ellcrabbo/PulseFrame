# PulseFrame

PulseFrame is a Flask-backed music visualiser that pairs offline waveform and spectrum plotting with a glowing, Web Audio API–powered live spectrum. Drop in a `.wav` file and the app renders high-res matplotlib plots server-side while the browser animates the full frequency range in real time.

## Features
- Upload `.wav` audio directly through the browser (no external services required).
- Generates waveform and log-scaled spectrum images with matplotlib using a dark theme.
- Adds a Web Audio API visualiser that highlights both low-end and treble activity.
- Persists uploads in `static/uploads/` with unique filenames for easy sharing.
- Works fully offline once dependencies are installed.

## Requirements
- Python 3.10+
- System libraries for `soundfile` (libsndfile) if not already present.

Install Python dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the App
```bash
python3 app.py
```

The development server runs at `http://127.0.0.1:5000/` by default. Open it in your browser, choose a `.wav` file, and click **Process Audio**. The page displays:
- The uploaded audio in a native HTML audio player.
- Live spectrum animation driven by `AnalyserNode`.
- Static waveform and spectrum plots rendered via matplotlib.

## Project Structure
```
PulseFrame/
├── app.py                 # Flask application and upload handling
├── visualiser.py          # Waveform + spectrum generation utilities
├── templates/index.html   # Self-contained UI, styles, and visualiser scripts
├── static/
│   └── uploads/           # Saved audio and generated plots
└── utils/                 # Additional audio tooling (optional helpers)
```

## Development Notes
- The Flask server saves each upload with a unique suffix to avoid collisions.
- `visualiser.generate_waveform_plot` applies a Hann window before FFT and outputs plots using the Agg backend.
- The live spectrum uses a 4096-point FFT with smoothing and emphasises high-frequency bins so treble activity remains visible.

## Troubleshooting
- **Flask not found**: Ensure the virtual environment is activated or reinstall dependencies with `pip install -r requirements.txt`.
- **No audio playback in browser**: Some browsers block autoplay without interaction—press play on the embedded audio control.
- **Missing soundfile backend**: Install the system package providing `libsndfile` (e.g., `brew install libsndfile` on macOS).

## License
See [LICENSE](LICENSE) for details.

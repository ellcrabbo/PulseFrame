import os
import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use("Agg")  # use non-GUI backend for Flask
import matplotlib.pyplot as plt


def generate_waveform_plot(audio_path):
    """Generate waveform and frequency spectrum images for a .wav file."""

    # Read audio file
    data, samplerate = sf.read(audio_path)

    # Handle stereo -> mono
    if data.ndim > 1:
        data = data.mean(axis=1)

    # === Waveform plot ===
    duration = len(data) / samplerate
    time = np.linspace(0, duration, len(data))

    plt.figure(figsize=(10, 3))
    plt.plot(time, data, color="#00ccff", linewidth=1)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(False)
    plt.tight_layout()

    waveform_path = os.path.join("static", "uploads", "waveform.png")
    plt.savefig(waveform_path, dpi=120, bbox_inches="tight", transparent=True)
    plt.close()

    # === Spectrum plot ===
    fft_data = np.abs(np.fft.rfft(data))
    freq = np.fft.rfftfreq(len(data), 1 / samplerate)

    plt.figure(figsize=(10, 3))
    plt.semilogx(freq, fft_data, color="#ffcc00", linewidth=1)
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(False)
    plt.tight_layout()

    spectrum_path = os.path.join("static", "uploads", "spectrum.png")
    plt.savefig(spectrum_path, dpi=120, bbox_inches="tight", transparent=True)
    plt.close()

    # Return both paths for Flask
    return waveform_path, spectrum_path
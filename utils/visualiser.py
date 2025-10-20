import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_waveform(samples, samplerate, original_name):
    """Draw a waveform + frequency spectrum snapshot."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), constrained_layout=True)

    # Time-domain waveform
    t = np.linspace(0, len(samples) / samplerate, num=len(samples))
    axes[0].plot(t, samples, color="#00ADB5")
    axes[0].set_title("Waveform")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Amplitude")

    # Frequency-domain spectrum (magnitude)
    freq = np.fft.rfftfreq(len(samples), 1/samplerate)
    spectrum = np.abs(np.fft.rfft(samples))
    axes[1].plot(freq, spectrum, color="#393E46")
    axes[1].set_xlim(0, samplerate / 4)
    axes[1].set_title("Frequency Spectrum")
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Magnitude")

    name = os.path.splitext(os.path.basename(original_name))[0] + ".png"
    out_path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return f"waveform/{name}"
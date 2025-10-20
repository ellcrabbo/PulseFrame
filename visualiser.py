from __future__ import annotations

import os
import uuid

import matplotlib

matplotlib.use("Agg")  # use non-GUI backend for Flask
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def _ensure_mono(data: np.ndarray) -> np.ndarray:
    """Collapse stereo signals into mono so plots remain readable."""
    if data.ndim > 1:
        return data.mean(axis=1)
    return data


def _build_output_path(output_dir: str, base_name: str, suffix: str) -> str:
    token = uuid.uuid4().hex[:8]
    filename = f"{base_name}_{suffix}_{token}.png"
    return os.path.join(output_dir, filename)


def generate_waveform_plot(audio_path: str, output_dir: str) -> tuple[str, str]:
    """Generate waveform and log-spectrum plots for a .wav file.

    Returns filenames relative to ``output_dir``.
    """
    os.makedirs(output_dir, exist_ok=True)

    data, samplerate = sf.read(audio_path)
    if data.size == 0:
        raise ValueError(f"No audio data found in {audio_path}")

    data = _ensure_mono(np.asarray(data))

    base_name = os.path.splitext(os.path.basename(audio_path))[0]

    # Waveform plot
    duration = len(data) / samplerate
    time = np.linspace(0, duration, len(data), endpoint=False)

    plt.style.use("dark_background")
    plt.figure(figsize=(10, 3))
    plt.plot(time, data, color="#00d0ff", linewidth=0.8)
    plt.title("Waveform", color="#f0f6fc")
    plt.xlabel("Time (s)", color="#8b949e")
    plt.ylabel("Amplitude", color="#8b949e")
    plt.tick_params(colors="#8b949e")
    plt.tight_layout()

    waveform_path = _build_output_path(output_dir, base_name, "waveform")
    plt.savefig(waveform_path, dpi=140, bbox_inches="tight", transparent=True)
    plt.close()

    # Spectrum plot
    windowed = data * np.hanning(len(data))
    fft_data = np.abs(np.fft.rfft(windowed))
    freq = np.fft.rfftfreq(len(windowed), 1 / samplerate)

    fft_data = np.maximum(fft_data, 1e-12)  # avoid log(0)

    plt.figure(figsize=(10, 3))
    plt.semilogx(freq, 20 * np.log10(fft_data), color="#f7b731", linewidth=0.8)
    plt.title("Frequency Spectrum", color="#f0f6fc")
    plt.xlabel("Frequency (Hz)", color="#8b949e")
    plt.ylabel("Magnitude (dB)", color="#8b949e")
    plt.tick_params(colors="#8b949e")
    plt.tight_layout()

    spectrum_path = _build_output_path(output_dir, base_name, "spectrum")
    plt.savefig(spectrum_path, dpi=140, bbox_inches="tight", transparent=True)
    plt.close()

    return os.path.basename(waveform_path), os.path.basename(spectrum_path)

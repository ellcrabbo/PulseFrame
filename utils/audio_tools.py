import soundfile as sf
import numpy as np

def read_wave(path):
    """Load a WAV file and return (samples, samplerate)."""
    data, samplerate = sf.read(path, dtype="float32")
    if data.ndim > 1:  # stereo → mono
        data = np.mean(data, axis=1)
    return data, samplerate
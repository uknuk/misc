#!/usr/bin/env python3


import numpy as np
import pyaudio
import sys

# Set up
volume = 1.0     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 5.0   # in seconds, may be float
f = float(sys.argv[1])        # sine frequency, Hz, may be float

# Generate samples
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# Create a stream object
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)

samples = volume*samples

# Play the stream
stream.write(samples.tobytes())

# Clean up
stream.stop_stream()
stream.close()
p.terminate()

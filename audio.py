import pyaudio
import numpy as np
import time


class Audio(object):
    """Audio device based on PyAudio"""

    def __init__(self, sample_rate=44100, buffer_size=128, volume=.8):
        assert volume < 1.0
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.volume = volume

    def start(self, callback, done, mode='blocking'):
        if mode == 'blocking':
            self.start_blocking(callback, done)
        if mode == 'callback':
            self.start_callback(callback, done)

    def start_blocking(self, callback, done):
        pa = pyaudio.PyAudio()
        stream = pa.open(rate=self.sample_rate, channels=1, format=pyaudio.paFloat32, output=1,
                         frames_per_buffer=self.buffer_size)
        t = 0.0
        while not done(t):
            ts = np.arange(self.buffer_size) / self.sample_rate + t
            y = np.array([callback(t) for t in ts])
            y *= self.volume
            stream.write(y.astype(np.float32).tobytes())
            t += self.buffer_size / self.sample_rate
        stream.stop_stream()
        stream.close()
        pa.terminate()

    def start_callback(self, callback, done):
        def stream_callback(in_data, frame_count, time_info, status):
            t = time_info['output_buffer_dac_time']
            ts = np.arange(frame_count) / self.sample_rate + t
            y = np.array([callback(t) for t in ts])
            y *= self.volume
            return y.astype(np.float32).tobytes(), done(t)
        pa = pyaudio.PyAudio()
        stream = pa.open(rate=self.sample_rate, channels=1, format=pyaudio.paFloat32, output=1,
                         frames_per_buffer=self.buffer_size, stream_callback=stream_callback)
        stream.start_stream()
        while stream.is_active():
            time.sleep(0.1)
        stream.stop_stream()
        stream.close()
        pa.terminate()

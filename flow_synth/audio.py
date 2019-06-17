import pyaudio
import numpy as np
import time


class Audio(object):
    """Audio device based on PyAudio.

    https://people.csail.mit.edu/hubert/pyaudio/docs/
    """

    def __init__(self, sample_rate=44100, buffer_size=128, volume=.8):
        """Create audio device.

        :param sample_rate int: Samples per second (Hz).
        :param buffer_size int: Size of the audio buffer.
        :param volume float: Number between 0 and 1 used to scale the audio output.
        """
        assert volume >= 0.0 and volume <= 1.0
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.volume = volume

    def start_stream(self, callback, done, mode='blocking'):
        """Start the audio stream.

        :param callback function: A function cb(t:float):float that produces an output signal.
        :param done function: A function d(t:float):bool that tells the audio to stop streaming.
        :param mode str: Select 'blocking' or 'callback' mode.
        """
        if mode == 'blocking':
            self.start_blocking_stream(callback, done)
        if mode == 'callback':
            self.start_callback_stream(callback, done)

    def start_blocking_stream(self, callback, done):
        """Start audio stream in blocking mode.

        The audio stream will block until it needs new audio data.

        :param callback function: A function cb(t:float):float that produces an output signal.
        :param done function: A function d(t:float):bool that tells the audio to stop streaming.
        """
        pa = pyaudio.PyAudio()
        stream = pa.open(rate=self.sample_rate, channels=1, format=pyaudio.paFloat32, output=1,
                         frames_per_buffer=self.buffer_size)
        t = 0.0
        # main loop
        while not done(t):
            ts = np.arange(self.buffer_size) / self.sample_rate + t # array of timesteps
            y = np.array([callback(t) for t in ts]) # compute output at each t
            y *= self.volume # scale output by volume
            stream.write(y.astype(np.float32).tobytes()) # write output to audio stream
            t += self.buffer_size / self.sample_rate # increment time
        # terminate
        stream.stop_stream()
        stream.close()
        pa.terminate()

    def start_callback_stream(self, callback, done):
        """Start audio stream in callback mode.

        The audio stream will run in a separate thread and call the callback function when it needs
        new audio data.

        :param callback function: A function cb(t:float):float that produces an output signal.
        :param done function: A function d(t:float):bool that tells the audio to stop streaming.
        """
        def stream_callback(in_data, frame_count, time_info, status):
            t = time_info['output_buffer_dac_time'] # get current time
            ts = np.arange(frame_count) / self.sample_rate + t # array of timesteps
            y = np.array([callback(t) for t in ts]) # compute output at each t
            y *= self.volume # scale output by volume
            return y.astype(np.float32).tobytes(), done(t) # return output buffer and done flag
        pa = pyaudio.PyAudio()
        stream = pa.open(rate=self.sample_rate, channels=1, format=pyaudio.paFloat32, output=1,
                         frames_per_buffer=self.buffer_size, stream_callback=stream_callback)
        stream.start_stream()
        while stream.is_active():
            time.sleep(0.1)
        stream.stop_stream()
        stream.close()
        pa.terminate()

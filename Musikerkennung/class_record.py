import numpy as np
import wave
import pyaudio


CHUNK = 1024
"""Number of frames to buffer before writing."""
FORMAT = pyaudio.paInt16
"""The data type used to record audio. See ``pyaudio`` for constants."""
CHANNELS = 1
"""The number of channels to record."""
RATE = 44100
"""The sample rate."""
RECORD_SECONDS = 10
"""Number of seconds to record."""
SAVE_DIRECTORY = "test/"
"""Directory used to save audio when using :func:`gen_many_tests`."""



class Record():
	# Initialises the class
	def __init__(self, filename: str):
		self.filename = filename
		self.frames = None

	########################################################################################
	# Only used functions
	########################################################################################

	def listen_to_song(self):
		""" Record 10 seconds of audio and optionally save it to a file

		:param filename: The path to save the audio (optional).
		:returns: The audio stream with parameters defined in this module.
		"""
		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK)

		print("* recording")

		frames = []
		write_frames = []

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(np.frombuffer(data, dtype=np.int16))
			if self.filename is not None:
				write_frames.append(data)

		print("* done recording")

		stream.stop_stream()
		stream.close()
		p.terminate()

		if self.filename is not None:
			wf = wave.open(self.filename, 'wb')
			wf.setnchannels(CHANNELS)
			wf.setsampwidth(p.get_sample_size(FORMAT))
			wf.setframerate(RATE)
			wf.writeframes(b''.join(frames))
			wf.close()

		self.frames = np.hstack(frames)
		return

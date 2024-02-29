import numpy as np
import wave

class Wave():
	def __init__(self, file_path: str = None) -> None:
		self.file_path = file_path
		self.signal = self.load(self.file_path)

	def load(self, file_path: str = None) -> None:
		spf = wave.open(file_path, 'r')
		signal = spf.readframes(-1)
		signal = np.frombuffer(signal, dtype=np.int16)
		print(f"numpy signal: {signal} {len(signal)}")
		downsampled_signal = signal[::100]
		print(f"numpy downsampled signal: {downsampled_signal} {len(downsampled_signal)}")
		return downsampled_signal

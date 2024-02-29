import argparse
import array
import math
import wave

import numpy as np
import pywt
from scipy import signal

class BPM():
	# Initialises the class
	def __init__(self, filename: str = None):
		self.filename = filename
		self.bpm = None
		self.bpm_median = None
		self.correl = None
		self.n = None

		parser = argparse.ArgumentParser()
		parser.add_argument("--window", type=float, default=3)
		parser.add_argument("--filename", type=str, default=self.filename)
		args = parser.parse_args()
		samps, fs = self.read_wav(args.filename)
		data = []
		correl = []
		bpm = 0
		n = 0
		nsamps = len(samps)

		window_samps = int(args.window * fs)
		# First sample in window_ndx
		samps_ndx = 0
		max_window_ndx = math.floor(nsamps / window_samps)
		bpms = np.zeros(max_window_ndx)

		# Iteriere über alle Fenster
		for window_ndx in range(0, max_window_ndx):
			# Get a new set of samples
			data = samps[samps_ndx : samps_ndx + window_samps]
			if not ((len(data) % window_samps) == 0):
				raise AssertionError(str(len(data)))

			bpm, correl_temp = self.bpm_detector(data, fs)
			if bpm is None:
				continue
			bpms[window_ndx] = bpm

			correl = correl_temp

			# Iterate at the end of the loop
			samps_ndx = samps_ndx + window_samps

			# Counter for debug...
			n += 1
		#print(bpms)
		self.bpm = bpms
		self.bpm_median = np.median(bpms)
		self.n = range(0, len(correl))
		self.correl = correl

########################################################################################
# Functions
########################################################################################

	# Function to read the wave file
	def read_wav(self, filename):
		# open file, get metadata for audio
		try:
			wf = wave.open(filename, "rb")
		except IOError as e:
			#print(e)
			return

		# typ = choose_type( wf.getsampwidth() ) # TODO: implement choose_typepeak_detect
		nsamps = wf.getnframes()
		assert nsamps > 0

		fs = wf.getframerate()
		assert fs > 0

		# Read entire file and make into an array
		samps = list(array.array("i", wf.readframes(nsamps)))

		try:
			assert nsamps == len(samps)
		except AssertionError:
			print(nsamps, "not equal to", len(samps))

		return samps, fs

	# print an error when no data can be found
	def no_audio_data(self):
		print("No audio data for sample, skipping...")
		return None, None

	# simple peak detection
	def peak_detect(self, data: array):
		max_val = np.amax(abs(data))
		peak_ndx = np.where(data == max_val)
		if len(peak_ndx[0]) == 0:  # if nothing found then the max must be negative
			peak_ndx = np.where(data == -max_val)
		return peak_ndx

	# Function to detect the bpm
	def bpm_detector(self, data, fs):
		cA = []
		cD = []
		correl = []
		cD_sum = []
		levels = 4
		max_decimation = 2 ** (levels - 1)
		min_ndx = math.floor(60.0 / 220 * (fs / max_decimation))
		max_ndx = math.floor(60.0 / 40 * (fs / max_decimation))

		for loop in range(0, levels):
			cD = []
			# 1) DWT
			if loop == 0:
				[cA, cD] = pywt.dwt(data, "db4")
				cD_minlen = len(cD) / max_decimation + 1
				cD_sum = np.zeros(math.floor(cD_minlen))
			else:
				[cA, cD] = pywt.dwt(cA, "db4")

			# 2) Filter
			cD = signal.lfilter([0.01], [1 - 0.99], cD)

			# 4) Subtract out the mean.

			# 5) Decimate for reconstruction later.
			cD = abs(cD[:: (2 ** (levels - loop - 1))])
			cD = cD - np.mean(cD)

			# 6) Recombine the signal before ACF
			#    Essentially, each level the detail coefs (i.e. the HPF values) are concatenated to the beginning of the array
			cD_sum = cD[0 : math.floor(cD_minlen)] + cD_sum

		if [b for b in cA if b != 0.0] == []:
			return self.no_audio_data()

		# Adding in the approximate data as well...
		cA = signal.lfilter([0.01], [1 - 0.99], cA)
		cA = abs(cA)
		cA = cA - np.mean(cA)
		cD_sum = cA[0 : math.floor(cD_minlen)] + cD_sum

		# ACF
		correl = np.correlate(cD_sum, cD_sum, "full")

		midpoint = math.floor(len(correl) / 2)
		correl_midpoint_tmp = correl[midpoint:]
		peak_ndx = self.peak_detect(correl_midpoint_tmp[min_ndx:max_ndx])
		if len(peak_ndx) > 1:
			return self.no_audio_data()

		peak_ndx_adjusted = peak_ndx[0] + min_ndx
		bpm = 60.0 / peak_ndx_adjusted * (fs / max_decimation)
		#print(bpm)

		return bpm, correl

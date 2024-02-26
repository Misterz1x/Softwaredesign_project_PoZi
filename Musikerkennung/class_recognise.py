import datetime
from tinytag import TinyTag
import logging
from multiprocessing import current_process
import numpy as np
from Musikerkennung.Speichern.class_save import Save
from Musikerkennung.class_fingerprint import Fingerprint as FP
from Musikerkennung.class_record import Record
import pygame as pg
from pytube import YouTube
from audio_extract import extract_audio
import os

class Recognise():
	# Initialises the class
	def __init__(self, file_link: str = None,  filename: str = None, song_info: tuple = None):
		self.file_link = file_link
		self.filename = filename
		self.song_info = song_info


########################################################################################
# Some of the functions are used only by other functions in this class
########################################################################################

	def get_song_info(self, filename):
		"""Gets the ID3 tags for a file. Returns None for tuple values that don't exist.

		:param filename: Path to the file with tags to read
		:returns: (artist, album, title)
		:rtype: tuple(str/None, str/None, str/None)
		"""
		tag = TinyTag.get(filename)
		artist = tag.artist if tag.albumartist is None else tag.albumartist
		return (artist, tag.album, tag.title)

	def score_match(self, offsets):
		"""Score a matched song.

		Calculates a histogram of the deltas between the time offsets of the hashes from the
		recorded sample and the time offsets of the hashes matched in the database for a song.
		The function then returns the size of the largest bin in this histogram as a score.

		:param offsets: List of offset pairs for matching hashes
		:returns: The highest peak in a histogram of time deltas
		:rtype: int
		"""
		# Use bins spaced 0.5 seconds apart
		binwidth = 0.5
		tks = list(map(lambda x: x[0] - x[1], offsets))
		hist, _ = np.histogram(tks,
								bins=np.arange(int(min(tks)),
											int(max(tks)) + binwidth + 1,
											binwidth))
		return np.max(hist)

########################################################################################
# Essential functions for the class
########################################################################################

	def best_match(self, matches):
		"""For a dictionary of song_id: offsets, returns the best song_id.

		Scores each song in the matches dictionary and then returns the song_id with the best score.

		:param matches: Dictionary of song_id to list of offset pairs (db_offset, sample_offset)
		as returned by :func:`~abracadabra.Storage.storage.get_matches`.
		:returns: song_id with the best score.
		:rtype: str
		"""
		matched_song = None
		best_score = 0
		try:
			for song_id, offsets in matches.items():
				if len(offsets) < best_score:
					# can't be best score, avoid expensive histogram
					continue
				score = self.score_match(offsets)
				if score > best_score:
					best_score = score
					matched_song = song_id
			return matched_song
		except Exception as e:
			logging.error(f"Error in best_match: {e}")
			raise TypeError("No Music found")

########################################################################################
# Functions to call from other classes
########################################################################################
	def register_song(self):
		"""Register a single song.

		Checks if the song is already registered based on path provided and ignores
		those that are already registered.

		:param filename: Path to the file to register"""
		if Save.song_in_db(self.filename):
			logging.info(f"{self.filename} is already registered. ({datetime.datetime.now()})")
			raise ValueError(f"{self.filename} is already registered")

		try:
			Fingerprint = FP(file_path=self.filename)
			Fingerprint.fingerprint_file()
			if self.song_info is None:
				self.song_info = self.get_song_info(self.filename)
			#print(self.filename)
			#print(self.song_info)
			File = Save(Fingerprint.hash_numbers(), self.song_info, self.filename)
			# log everything
			logging.info(f"{current_process().name} waiting to write {self.filename}. ({datetime.datetime.now()}")
				# running single-threaded, no lock needed
			File.save_to_db()
			logging.info(f"{current_process().name} done writing {self.filename}. ({datetime.datetime.now()})")
		except Exception as e:
			logging.error(f"Error in register_song: {e}")
			raise e

	def download_audio(self):
		try:
			logging.info(f"Download {self.file_link}. ({datetime.datetime.now()})")
			yt = YouTube(self.file_link)
			video = yt.streams.filter(only_audio=True).first()
			video.download(output_path = "Musik")
			audio_path = os.path.join("Musik", video.default_filename)
			self.filename = audio_path
			if video.default_filename in os.listdir("Musik"):
				actual_filename = self.filename[:-4]
				if(self.filename.endswith(".mp4")):
					extract_audio(input_path=self.filename, output_path=actual_filename + ".wav", output_format="wav")
					self.filename = actual_filename + ".wav"
					os.remove(audio_path)
			self.song_info = {"artist": yt.author, "title": yt.title, "file_link": self.file_link}
			logging.info(f"Downloaded {video.title}. ({datetime.datetime.now()})")
			return
		except Exception as e:
			logging.error(f"Error in download_audio: {e}")
			raise e

	def recognise_song(self):
		"""Recognises a pre-recorded sample.

		Recognises the sample stored at the path ``filename``. The sample can be in any of the
		formats in :data:`recognise.KNOWN_FORMATS`.

		:param filename: Path of file to be recognised.
		:returns: :func:`~abracadabra.recognise.get_song_info` result for matched song or None.
		:rtype: tuple(str, str, str)
		"""
		try:
			logging.info(f"Discover the fingerprint of {self.filename}. ({datetime.datetime.now()})")
			Fingerprint = FP(file_path=self.filename)
			Fingerprint.fingerprint_file()
			#print(hashes[0])
			logging.info(f"Find matches for {self.filename}. ({datetime.datetime.now()})")
			matches = Save.get_matches(hashes = Fingerprint.hash_numbers())
			matched_song = self.best_match(matches)
			self.song_info = Save.get_song_info(matched_song)
			self.filename = self.song_info.file_path
			logging.info(f"Matched {self.filename}")
		except Exception as e:
			logging.error(f"Error in recognise_song: {e}. ({datetime.datetime.now()})")
			raise e
		return


	# To get to play the song
	def listen_to_song(self):
		"""Recognises a song using the microphone.

		Optionally saves the sample recorded using the path provided for use in future tests.
		This function is good for one-off recognitions, to generate a full test suite, look
		into :func:`~abracadabra.record.gen_many_tests`.

		:param filename: The path to store the recorded sample (optional)
		:returns: :func:`~abracadabra.recognise.get_song_info` result for matched song or None.
		:rtype: tuple(str, str, str)
		"""
		try:
			RE = Record(self.filename)
			RE.listen_to_song()
			Fingerprint = FP(RE.filename)
			Fingerprint.fingerprint_file()

			logging.info(f"Find matches for {self.filename}. ({datetime.datetime.now()})")
			matches = Save.get_matches(hashes = Fingerprint.hash_numbers())
			matched_song = self.best_match(matches)
			self.song_info = Save.get_song_info(matched_song)
			try:
				self.filename = self.song_info.file_path
			except Exception as e:
				raise AttributeError(f"Song not found in database.")
			logging.info(f"Matched {self.filename}")
		except Exception as e:
			logging.error(f"Error in recognise_song: {e}. ({datetime.datetime.now()})")
			raise e
		return

	def song_data(self):
		return self.song_info

	def play_song(self, file_path, play_duration = 10000):
		"""Play a song using pygame.

		:param file_path: Path of the song to be played.
		:param play_duration: The duration of the song to be played.
		"""
		pg.init()
		pg.mixer.init()
		pg.mixer.music.load(file_path)
		pg.mixer.music.play()
		if play_duration:
			pg.time.wait(play_duration)
			pg.mixer.music.stop()
		else:
			while pg.mixer.music.get_busy():
				for event in pg.event.get():
					if event.type == pg.KEYDOWN:
						print("Musik beendet")
						pg.mixer.music.stop()

import os
from Speichern.class_save import Save
from datetime import datetime
from tinytag import TinyTag
from Speichern.serializer import serializer
from settings import KNWON_EXTENSIONS, NUM_WORKERS
import logging
from multiprocessing import current_process, Lock, Pool
import numpy as np

class Recognise():

	# Class variable that is shared between all instances of the class
	def __init__(self, file_path: str):
		self.file_path = file_path

	# Method to get the file extension
	def get_extension_info(self):
		# Get the file extension
		file_extension = os.path.splitext(self.file_path)[1][1:]
		# Check if the file extension is in the list of known file extensions
		if file_extension in KNWON_EXTENSIONS:
			return True
		else:
			return None

	# Method to get the song info
	def get_song_info(self):
		tag = TinyTag.get(self.file_path)
		# Get the info for the song
		artist = tag.artist if tag.albumartist is None else tag.albumartist
		return (artist, tag.album, tag.title)

	# Method to register a song
	def register_song(self, file_path: str):
		if Save.song_in_db(file_path):
			print('Song already in database')
			return
		hashes = fingerprint_file(file_path)
		song_info = self.get_song_info()

		logging.info(f'{current_process().name} - Saving song: {song_info[2]} by {song_info[0]}')

		Save(hashes, song_info, file_path).save_to_db()

		logging.info(f'{current_process().name} - Song saved: {song_info[2]} by {song_info[0]}')


	# Method to register a directory
	def register_dir(self):
		# Create a lock
		def pool_init(l):
			global lock
			lock = l
			logging.info(f"Pool init in {current_process().name}")

		# Get the file extension
		if self.get_extension_info():
			l = Lock()
			# Register the song
			with Pool(NUM_WORKERS, initializer= pool_init, initargs= (l,)) as p:
				p.map(self.register_song, self.file_path)

	# Method to get the matches of the recorded song
	def score_match(offsets):
		"""Score a matched song.

		Calculates a histogram of the deltas between the time offsets of the hashes from the
		recorded sample and the time offsets of the hashes matched in the database for a song.
		The function then returns the size of the largest bin in this histogram as a score.

		:param offsets: List of offset pairs for matching hashes
		:returns: The highest peak in a histogram of time deltas
		:rtype: int
		"""
		binwidth = 0.5
		tks = list(map(lambda x: x[0] - x[1], offsets))
		hist, _ = np.histogram(tks,
								bins=np.arange(int(min(tks)),
											int(max(tks)) + binwidth + 1,
											binwidth))
		return np.max(hist)

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
		for song_id, offsets in matches.items():
			if len(offsets) < best_score:
				# can't be best score, avoid expensive histogram
				continue
			score = self.score_match(offsets)
			if score > best_score:
				best_score = score
				matched_song = song_id
		return matched_song

	def recognise_song(self, file_path: str):
		"""Recognises a pre-recorded sample.

		Recognises the sample stored at the path ``filename``. The sample can be in any of the
		formats in :data:`recognise.KNOWN_FORMATS`.

		:param filename: Path of file to be recognised.
		:returns: :func:`~abracadabra.recognise.get_song_info` result for matched song or None.
		:rtype: tuple(str, str, str)
		"""
		hashes = fingerprint_file(file_path)
		matches = Save.get_matches(hashes)
		matched_song = self.best_match(matches)
		info = Save.get_song_info(matched_song)
		if info is not None:
			return info
		return matched_song

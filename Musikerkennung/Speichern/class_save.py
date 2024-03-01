import logging
import os
from tinydb import TinyDB, Query
from Musikerkennung.Speichern.serializer import serializer
import datetime


class Save():
	#Class variable that is shared between all instances of the class
	db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage = serializer)

	def __init__(self, hashes: list = None, song_info: list = None, file_path: str = None, last_viewed: datetime = None):
		if hashes is not None and file_path is not None:
			self.hashes = hashes
			self.song_info = song_info
			self.file_path = file_path
			self.last_viewed = last_viewed
			self.is_active = False
		elif hashes is None:
			self.is_active = True
			self.song_info = song_info
			self.file_path = file_path

	# String representation of the class
	def __str__(self):
		return f'Song: {self.song_info["title"]} by {self.song_info["artist"]}'

	# String representation of the class
	def __repr__(self):
		return self.__str__()

	# Method to save the data to the database
	def save_to_db(self):
		#Create a table in the database
		table_hashes = self.db_connector.table('hashes')
		#Create a table in the database for the song info
		table_song_data = Save.db_connector.table('song_info')
		#Create a dictionary to store the data
		query = Query()
		#Create the result variable
		result = None
		#Check if the song is already in the database
		try:
			if self.is_active:
				result = table_song_data.search(query.song_id == self.song_info['song_id'])
			else:
				result = table_song_data.search(query.song_id == self.hashes[0]['song_id'])
		except Exception as e:
			raise TypeError(f"Error in save_to_db searching for song_data: {e}")
		#If the song is not in the database, add it
		try:
			if result:
				print('Song already in database')
			else:
				table_hashes.insert_multiple(self.hashes)
		except Exception as e:
			raise TypeError(f"Error in save_to_db inserting hashes: {e}")
		# Store the song info in the database
		try:
			if not result:
				#Create a dictionary to store the data
				song_data = {'artist': self.song_info['artist'], 'title': self.song_info['title'], 'last_viewed': self.last_viewed,'file_link': self.song_info['file_link'],'cover_url': self.song_info['cover_url'], 'song_id': self.hashes[0]['song_id'],'file_path': self.file_path}
				# Store the data
				table_song_data.insert(song_data)
			elif result and self.is_active:
				song_data_update = {'artist': self.song_info['artist'], 'title': self.song_info['title'], 'last_viewed': self.song_info['last_viewed'],'file_link': self.song_info['file_link'],'cover_url': self.song_info['cover_url'], 'song_id': self.song_info['song_id'],'file_path': self.song_info['file_path']}
				table_song_data.update(song_data_update, doc_ids=[result[0].doc_id])
		except Exception as e:
			raise TypeError(f"Error in save_to_db inserting song_data: {e}")

	def get_info(self):
		return self.song_info


	@classmethod
	def get_song_info(cls, song_id):
		#Create a table in the database
		table = cls.db_connector.table('song_info')
		#Create a dictionary to store the data
		query = Query()
		#Check if the song is already in the database
		result = table.search(query.song_id == song_id)
		#If the song is not in the database, add it
		#print(result)
		if result:
			data = result[0]
			return cls(song_info = data, file_path = data['file_path'])
		else:
			return None

	# Method to find out if the path i already in the database
	@classmethod
	def song_in_db(cls, file_path: str):
		#Create a table in the database
		table = cls.db_connector.table('song_info')
		#Create a dictionary to store the data
		query = Query()
		#Check if the song is already in the database
		result = table.search(query.file_path == file_path)
		#If the song is not in the database, return false
		if result:
			return True
		else:
			return False

	# Method to get matches of the compared song
	@classmethod
	def get_matches(cls, hashes, min_matches = 15):
		matches_dict = {}
		h_dict = {}
		#Search for the songs in the database
		table_info = cls.db_connector.table('song_info')
		table_hashes = cls.db_connector.table('hashes')
		query = Query()
		result = table_info.all()
		lenght_hashes = len(hashes)
		for i in range(len(hashes)):
			h_dict[hashes[i]['hash']] = hashes[i]['offset']

		if result:
			for song in range(len(result)):

				# Search for the song in the database
				selected_song = table_hashes.search(query.song_id == result[song]['song_id'])

				matches = []
				# Compare the hashes
				for hash in range(len(selected_song[: -lenght_hashes])):

					# Compare the hashes
					for i in range(lenght_hashes):
						if selected_song[hash + i]['hash'] == hashes[i]['hash']:

							# Count the number of matches
							matches.append((selected_song[hash + i]['offset'], h_dict[selected_song[hash + i]['hash']]))
					# Save the number of matches in a dictionary if the number of matches is greater than a specific number
				if len(matches) >= min_matches:
					matches_dict[result[song]['song_id']] = matches
					matches = {}
					continue
			# Return the dictionary
			return matches_dict
		else:
			return None

	@classmethod
	def get_all(cls):
		#Create a list of all the songs
		song_info = []
		#Create a table in the database
		table_songs = cls.db_connector.table('song_info')
		#Check if the song is already in the database
		result = table_songs.all()
		#If the song is not in the database, add it
		for song in result:
			song_info.append(cls(song_info = song, file_path = song['file_path']))
		if result:
			return song_info
		else:
			return None

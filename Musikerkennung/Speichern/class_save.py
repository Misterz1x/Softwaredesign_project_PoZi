import os
from tinydb import TinyDB, Query
from Musikerkennung.Speichern.serializer import serializer


class Save():
	#Class variable that is shared between all instances of the class
	db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage = serializer)

	def __init__(self, hashes: list = None, song_info: list = None, file_path: str = None):
		if hashes is not None and file_path is not None:
			self.hashes = hashes
			self.song_info = song_info
			self.file_path = file_path
		elif hashes is None:
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
		table = self.db_connector.table('hashes')
		#Create a dictionary to store the data
		query = Query()
		#Check if the song is already in the database
		result = table.search(query.song_id == self.hashes[0]['song_id'])
		#If the song is not in the database, add it
		if result:
			print('Song already in database')
		else:
			table.insert_multiple(self.hashes)
		# Store the song info in the database
		if not result:
			#Create a table in the database for the song info
			table = Save.db_connector.table('song_info')
			#Create a dictionary to store the data
			song_data = {'artist': self.song_info[0], 'title': self.song_info[1], 'album': self.song_info[2], 'song_id': self.hashes[0]['song_id'],'file_path': self.file_path}
			# Store the data
			table.insert(song_data)

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
	def get_matches(cls, hashes, min_matches = 10):
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

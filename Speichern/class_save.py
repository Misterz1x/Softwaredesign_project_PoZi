import os
from tinydb import TinyDB, Query
from datetime import datetime
from serializer import serializer


class Save():
	#Class variable that is shared between all instances of the class
	db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage = serializer)

	def __init__(self, hashes: list, song_info: list, file_path: str):
		self.hashes = {'hash': hashes[0], 'offset': hashes[1], 'song_id': hashes[2]}
		self.song_info = {'artist': song_info[0], 'title': song_info[1], 'album': song_info[2], 'song_id': hashes[0][2], 'file_path': file_path}

	# Method to get the song info
	def __init__(self, song_info: str):
		self.song_info = song_info

	# String representation of the class
	def __str__(self):
		return f'Song: {self.song_info["title"]} by {self.song_info["artist"]}'

	# String representation of the class
	def __repr__(self):
		return self.__str__()

	# Method to save the data to the database
	def save_to_db(self):
		#Create a table in the database
		table = Save.db_connector.table('hashes')
		#Create a dictionary to store the data
		Query = Query()
		#Check if the song is already in the database
		result = table.search(Query.song_id == self.hashes['song_id'])
		#If the song is not in the database, add it
		if result:
			print('Song already in database')
		else:
			table.insert(self.hashes)
		# Store the song info in the database
		if not result:
			#Create a table in the database for the song info
			table = Save.db_connector.table('song_info')
			# Store the data
			table.insert(self.song_info)



	@classmethod
	def get_song_info(cls, song_id):
		#Create a table in the database
		table = Save.db_connector.table('song_info')
		#Create a dictionary to store the data
		Query = Query()
		#Check if the song is already in the database
		result = table.search(Query.song_id == song_id)
		#If the song is not in the database, add it
		if result:
			return cls(result)
		else:
			return None

	# Method to find out if the path i already in the database
	@classmethod
	def song_in_db(file_path: str):
		#Create a table in the database
		table = Save.db_connector.table('song_info')
		#Create a dictionary to store the data
		Query = Query()
		#Check if the song is already in the database
		result = table.search(Query.file_path == file_path)
		#If the song is not in the database, return false
		if result:
			return True
		else:
			return False

	# Method to get matches of the compared song
	@classmethod
	def get_matches(hashes, threshold: int = 5):
		matches_dict = {}
		#Search for the songs in the database
		table = Save.db_connector.table('song_info')
		Query = Query()
		result = table.all()
		# If there are songs in the database, save the id in a list
		song_id = result['song_id']
		# Swap the table
		table = Save.db_connector.table('hashes')
		if result:
			for song in song_id:
				# Search for the song in the database
				result = table.search(Query.song_id == song)
				# Compare the hashes
				for hash in result:
					# Compare the hashes
					if hash['hash'] == hashes['hash']:
						# Count the number of matches
						matches += 1
				# Save the number of matches in a dictionary if the number of matches is greater than a specific number
				if matches >= threshold:
					matches_dict[song] = matches
			# Return the dictionary
			return matches_dict
		else:
			return None

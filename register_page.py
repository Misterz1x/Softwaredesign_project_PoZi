import logging
import streamlit as st
import time
import pandas as pd
from Musikerkennung.class_recognise import Recognise
from Musikerkennung.Speichern.class_save import Save
from settings import KNOWN_EXTENSIONS
import os

############################################################################################
# Streamlit page setup
############################################################################################

st.set_page_config( page_title="Upload your Song", page_icon=":musical_note:", layout="wide")

cl1, cl2 = st.columns([1, 1])

cl1.title("Upload your songs!")
cl1.markdown(
	"""
	This page allows you to upload songs that will be processed and stored into our database.
	Afterwards you can use the 'Find your song' page to try and recognise those songs.
	"""
	)

if 'show_reg' not in st.session_state:
	st.session_state.show_reg = 0

# Define the placeholders
button_ph = cl1.empty()
file_ph = cl1.empty()
cl5, cl6 = cl1.columns([1, 1])
title_ph = cl5.empty()
artist_ph = cl6.empty()
cl3, cl4 = cl1.columns([1, 6])
button_save = cl3.empty()
button_back = cl4.empty()
button_Save_file = cl3.empty()
error_file_save_ph = cl4.empty()
error_ph = cl1.empty()

##########################################################################
# Functions
##########################################################################

def register_file():
	uploaded_file = file_ph.file_uploader("Upload a wav-file or a folder", type=KNOWN_EXTENSIONS)
	if uploaded_file is not None:
	# To read file as bytes:
		file_path = os.path.join("Musik", uploaded_file.name)
		with open(file_path, "wb") as f:
			f.write(uploaded_file.getbuffer())
		return file_path

def upload_file(file_path, song_info):
	if file_path is not None:
		Rec = Recognise(filename=file_path, song_info=song_info)
		try:
			with st.spinner('Processing...'):
				Rec.register_song()
				error_ph.success('Done!')
		except Exception as e:
			error_ph.error(f"Error: {e}")

############################################################################################
# Continues to list data permanently
############################################################################################

# View the last viewed songs
cl2.title("Registered songs:")
#Create a dictionary to list the songs
try:
	data_list = []
	#Get the songs from the database
	songs = Save.get_all()
	#Create a dataframe to store the songs
	for song in songs:
		data_list.append({'Title': song.song_info['title'], 'Artist': song.song_info['artist'], 'File Link': song.song_info['file_link']})
	#Create a dataframe to store the songs
	df = pd.DataFrame(data_list)
	#Display the dataframe
	cl2.data_editor(df, hide_index=True, disabled = ("Title", "Artist"))
except Exception as e:
	logging.error(f"Error in register_page: {e}")
	cl2.info("No songs registered yet.")

##########################################################################
# Main
##########################################################################

if st.session_state.show_reg == 0:
	uploaded_file = register_file()
	title = title_ph.text_input("Title of the song", placeholder="Title...", )
	artist = artist_ph.text_input("Artist of the song", placeholder="Artist...")
	if button_Save_file.button("Save") and uploaded_file is not None and title is not None:
		song_info = {"title": title, "artist": artist, "file_link": None, "cover_url": None}
		upload_file(uploaded_file, song_info)
		time.sleep(2)
		st.rerun()
	else:
		error_file_save_ph.info("Please upload a file and enter a title.")

	if button_ph.button("Save Link"):
		st.session_state.show_reg = 1
		file_ph.empty()
		error_ph.empty()
		button_save.empty()
		st.rerun()

if st.session_state.show_reg == 1:
	file_link = button_ph.text_input("Link to the song", placeholder="Link...")
	if button_save.button("Save"):
		Rec = Recognise(file_link)
		try:
			with st.spinner('Processing...'):
				Rec.download_audio()
				Rec.register_song()
				st.success('Done!')
				time.sleep(2)
				st.rerun()
		except Exception as e:
			st.error(f"Error: {e}")

	if button_back.button("Back"):
		st.session_state.show_reg = 0
		button_save.empty()
		button_ph.empty()
		st.rerun()

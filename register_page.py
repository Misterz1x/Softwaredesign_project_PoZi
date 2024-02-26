import streamlit as st
import time
from Musikerkennung.class_recognise import Recognise

from settings import KNOWN_EXTENSIONS
import os

st.set_page_config( page_title="Upload your Song", page_icon=":musical_note:")

st.title("Upload your songs!")
st.markdown(
	"""
	This page allows you to upload songs that will be processed and stored into our database.
	Afterwards you can use the 'Find your song' page to try and recognise those songs.
	"""
	)

if 'show_reg' not in st.session_state:
	st.session_state.show_reg = 0

# Define the placeholders
button_ph = st.empty()
file_ph = st.empty()
cl1, cl2 = st.columns([1, 6])
button_save = cl1.empty()
button_back = cl2.empty()
error_ph = st.empty()

##########################################################################
# Functions
##########################################################################

def register_file():
	uploaded_file = file_ph.file_uploader("Upload a wav-file or a folder", type=KNOWN_EXTENSIONS,)
	if uploaded_file is not None:
	# To read file as bytes:
		file_path = os.path.join("Musik", uploaded_file.name)
		with open(file_path, "wb") as f:
			f.write(uploaded_file.getbuffer())
		return file_path

def upload_file(file_path):
	if file_path is not None:
		Rec = Recognise(file_path)
		try:
			with st.spinner('Processing...'):
				Rec.register_song()
				error_ph.success('Done!')
		except Exception as e:
			error_ph.error(f"Error: {e}")

def upload_link(file_link):
	Rec = Recognise(file_link)
	try:
		with st.spinner('Processing...'):
			Rec.download_audio()
			Rec.register_song()
			st.success('Done!')
			time.sleep(2)
	except Exception as e:
		st.error(f"Error: {e}")

##########################################################################
# Main
##########################################################################

if st.session_state.show_reg == 0:
	uploaded_file = register_file()
	if uploaded_file is not None:
		upload_file(uploaded_file)
	if button_ph.button("Save Link"):
		st.session_state.show_reg = 1
		file_ph.empty()
		error_ph.empty()

if st.session_state.show_reg == 1:
	file_link = button_ph.text_input("Link to the song", placeholder="Link...")
	if button_save.button("Save"):
		upload_link(file_link)
		time.sleep(2)

	if button_back.button("Back"):
		st.session_state.show_reg = 0
		button_save.empty()
		button_ph.empty()
		st.rerun()

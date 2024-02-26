
import os
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from settings import KNOWN_EXTENSIONS
from Musikerkennung.class_recognise import Recognise as recog
from pydub import AudioSegment

st.set_page_config( page_title="Find your song", page_icon="🔮")



st.title("We'll find your song!")
st.markdown(
	"""
	This page allows you to upload songs or snippets with the 'Recognise' button. If the song is in our database
	(using the 'Upload your songs' page) we'll try to tell you which song it is.

	If you press the 'Activate Microphone' button we actively listen to your song and we'll try to recognise it.
	""")

if 'show_session_rec' not in st.session_state:
	st.session_state.show_session_rec = 0

# Define the placeholders
button1_ph = st.empty()
file_ph = st.empty()
info_ph = st.empty()
play_ph = st.empty()
button2_ph = st.empty()

def register_file():
	uploaded_file = file_ph.file_uploader("Upload a wav-file or a folder", type=KNOWN_EXTENSIONS)
	if uploaded_file is not None:
	# To read file as bytes:
		file_path = os.path.join("Musik", uploaded_file.name)
		with open(file_path, "wb") as f:
			f.write(uploaded_file.getbuffer())
		return file_path

def delete_file_in_folder(file_path):
	if file_path is not None:
		os.remove(file_path)

def recognise_music(file_path):
	if file_path is not None:
		Rec = recog(file_path)
		try:
			with st.spinner('Processing...'):
				Rec.recognise_song()
				delete_file_in_folder(file_path)
			if Rec.song_data().song_info['title'] is not None and Rec.song_data().song_info['artist'] is not None:
				info_ph.success(f'Song recognised! We think it is: {Rec.song_data().song_info['title']} by {Rec.song_data().song_info['artist']}')
			else:
				info_ph.success(f'Song recognised! We think it is: {Rec.filename}')
			# Add the song to the audio_transmitter
			audio_data = AudioSegment.from_file(Rec.filename)
			duration = len(audio_data) / 1000
			play_ph.audio(Rec.filename, format='audio/wav')

		except Exception as e:
			info_ph.error(f"Error: {e}")

def listening_button():
	#add recongnise code
	with st.spinner('Listening...'):
		try:
			Rec = recog(filename="Musik/recorded_song.wav")
			Rec.listen_to_song()
			delete_file_in_folder("Musik/recorded_song.wav")
			if Rec.song_data().song_info['title'] is not None and Rec.song_data().song_info['artist'] is not None:
				print(Rec.song_data())
				info_ph.success(f'Song recognised! We think it is: {Rec.song_data().song_info['title']} by {Rec.song_data().song_info['artist']}, Link to Youtube: {Rec.song_data().song_info['file_link']}')
			else:
				info_ph.success(f'Song recognised! We think it is: {Rec.filename}')
			# Add the song to the audio_transmitter
			audio_data = AudioSegment.from_file(Rec.filename)
			duration = len(audio_data) / 1000
			play_ph.audio(Rec.filename, format='audio/wav')
		except Exception as e:
			info_ph.warning(f"{e}")
			delete_file_in_folder("Musik/recorded_song.wav")

if st.session_state.show_session_rec == 0:
	uploaded_file = register_file()
	if uploaded_file is not None:
		button2_ph.empty()
		recognise_music(uploaded_file)
	if button2_ph.button("Activate Microphone"):
		st.session_state.show_session_rec = 1
		button2_ph.empty()
		file_ph.empty()
		st.rerun()

if st.session_state.show_session_rec == 1:
	if button1_ph.button("Recognise"):
		st.session_state.show_session_rec = 0
		button1_ph.empty()
		file_ph.empty()
		st.rerun()
	if button2_ph.button("Activate Microphone"):
		listening_button()

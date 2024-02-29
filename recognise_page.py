
import os
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
import logging
from settings import KNOWN_EXTENSIONS
from Musikerkennung.class_recognise import Recognise as recog
from Musikerkennung.Speichern.class_save import Save
from Musikerkennung.class_bpm import BPM
from Musikerkennung.class_Wav import Wave
from pydub import AudioSegment
import pandas as pd

############################################################################################
# Streamlit page setup
############################################################################################

st.set_page_config( page_title="Find your song", page_icon="🔮", layout = "wide")
#Page width
cl1, cl2 = st.columns([1, 1])

cl1.title("We'll find your song!")
cl1.markdown(
	"""
	This page allows you to upload songs or snippets with the 'Recognise' button. If the song is in our database
	(using the 'Upload your songs' page) we'll try to tell you which song it is.

	If you press the 'Activate Microphone' button we actively listen to your song and we'll try to recognise it.
	""")

if 'show_session_rec' not in st.session_state:
	st.session_state.show_session_rec = 0

# Define the placeholders
button1_ph = cl1.empty()
button2_ph = cl1.empty()
Cover_ph = cl1.empty()
file_ph = cl1.empty()
info_ph = cl1.empty()
play_ph = cl1.empty()
chart_wave_ph = cl1.empty()
chart_bpm_ph = cl1.empty()

############################################################################################
# Functions
############################################################################################

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
	Rec = recog(filename=file_path)
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
		if st.button("View the charts"):
			with st.spinner('Generate Wave Chart ...'):
				# Print the Wave Chart
				wave = Wave(Rec.filename)
				chart2_data = pd.DataFrame({"Amplitude" : wave.signal})
				chart_wave_ph.line_chart(chart2_data, use_container_width=True)
				# Print the BPM
			with st.spinner('Generate BPM Chart ...'):
				bpm = BPM(Rec.filename)
				chart_data = pd.DataFrame({"Zeitfenster": len(bpm.bpm), "BPM" : bpm.bpm})
				chart_bpm_ph.line_chart(chart_data)
				st.write(f"The BPM of the song is: {bpm.bpm_median}")
	except Exception as e:
		info_ph.error(f"Error: {e}")

def listening_button():
	#add recongnise code
	try:
		with st.spinner('Listening...'):
			Rec = recog(filename="Musik/recorded_song.wav")
			Rec.listen_to_song()
			delete_file_in_folder("Musik/recorded_song.wav")
			if Rec.song_data().song_info['title'] is not None and Rec.song_data().song_info['artist'] is not None:
				print(Rec.song_data())
				info_ph.success(f'Song recognised! We think it is: {Rec.song_data().song_info['title']} by {Rec.song_data().song_info['artist']}, Link to Youtube: {Rec.song_data().song_info['file_link']}')
			else:
				info_ph.success(f'Song recognised! We think it is: {Rec.filename}')
			Cover_ph.image(Rec.song_data().song_info['cover_url'], width=200)
			# Add the song to the audio_transmitter
			audio_data = AudioSegment.from_file(Rec.filename)
			duration = len(audio_data) / 1000
			play_ph.audio(Rec.filename, format='audio/wav')
		with st.spinner('Generate Wave Chart ...'):
			# Print the Wave Chart
			try:
				wave = Wave(Rec.filename)
				chart2_data = pd.DataFrame({"Amplitude" : wave.signal})
				chart_wave_ph.line_chart(chart2_data, use_container_width=True)
			except Exception as e:
				logging.info(f"File deleted")
			# Print the BPM
		with st.spinner('Generate BPM Chart ...'):
			try:
				bpm = BPM(Rec.filename)
				chart_data = pd.DataFrame({"Zeitfenster": len(bpm.bpm), "BPM" : bpm.bpm})
				chart_bpm_ph.line_chart(chart_data)
				st.write(f"The BPM of the song is: {bpm.bpm_median}")
			except Exception as e:
				logging.info(f"File deleted: {e}")
	except Exception as e:
		info_ph.warning(f"{e}")
		try:
			delete_file_in_folder("Musik/recorded_song.wav")
		except Exception as e:
			logging.warning(f"Song already deleted")

############################################################################################
# Continues to list data permanently
############################################################################################

# View the last viewed songs
cl2.title("Your last viewed songs")
#Create a dictionary to list the songs
try:
	data_list = []
	#Get the songs from the database
	songs = Save.get_all()
	#Create a dataframe to store the songs
	for song in songs:
		if song.song_info['last_viewed'] is not None:
			data_list.append({'Title': song.song_info['title'], 'Artist': song.song_info['artist'], 'Last viewed': song.song_info['last_viewed']})
	#Create a dataframe to store the songs
	df = pd.DataFrame(data_list)
	df = df.sort_values(by='Last viewed', ascending=False)
	#Display the dataframe
	cl2.data_editor(df, hide_index=True, disabled = ("Title", "Artist", "Last viewed"))
except Exception as e:
	cl2.info("No songs registered yet.")

############################################################################################
# Streamlit switch between the states
############################################################################################

# State to identify another file
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

# State to listen to the song
if st.session_state.show_session_rec == 1:
	if button1_ph.button("Recognise"):
		st.session_state.show_session_rec = 0
		button1_ph.empty()
		file_ph.empty()
		st.rerun()
	if button2_ph.button("Activate Microphone"):
		info_ph.empty()
		chart_wave_ph.empty()
		chart_bpm_ph.empty()
		listening_button()

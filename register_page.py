from st_pages import Page, add_page_title, show_pages
import streamlit as st
import time
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
import Musikerkennung.class_recognise as recog
from io import StringIO
from settings import KNOWN_EXTENSIONS
import os
from pydub import AudioSegment



st.set_page_config( page_title="Upload your Song", page_icon=":musical_note:")


st.title("Upload your songs!")
st.markdown(
    """
    This page allows you to upload songs that will be processed and stored into our database. 
    Afterwards you can use the 'Find your song' page to try and recognise those songs.
    """
    )


if 'show_session_reg' not in st.session_state:
    st.session_state.show_session_reg = 0

# Define the placeholders
#button_ph = st.empty()
file_ph = st.empty()

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
		Rec = recog.Recognise(file_path)
		try:
			with st.spinner('Processing...'):
				Rec.register_song()
				st.success('Done!')
		except Exception as e:
			st.error(f"Error: {e}")


##########################################################################
# Main
##########################################################################

if st.session_state.show_session_reg == 0:
	uploaded_file = register_file()
	if uploaded_file is not None:
		upload_file(uploaded_file)
	#if button_ph.button("Save Link"):
	#	st.session_state.show_session = 1
	#	file_ph.empty()

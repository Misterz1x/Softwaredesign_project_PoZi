from st_pages import Page, add_page_title, show_pages
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header



st.title("We'll find your song!")
st.markdown(
    """
    This page allows you to upload songs or snippets with the 'Recognise' button. If the song is in our database 
    (using the 'Upload your songs' page) we'll try to tell you which song it is. 

    If you press the 'Activate Microphone' button we actively listen to your song and we'll try to recognise it. 
    """)

def recognise_button():
    uploaded_file = st.file_uploader("Upload a wav-file or a folder")


def listening_button():
    #add recongnise code
    st.write("Wavecraft is listening")


def main():

    if st.button("Recognise"):
        recognise_button()

    if st.button("Activate Microphone"):
        listening_button()

if __name__ == "__main__":
    main()
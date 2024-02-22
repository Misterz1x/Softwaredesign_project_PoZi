from st_pages import Page, add_page_title, show_pages
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header



st.title("Upload your songs!")
st.markdown(
    """
    This page allows you to upload songs that will be processed and stored into our database. 
    Afterwards you can use the 'Find your song' page to try and recognise those songs.
    """
    )


def register_page(): 
    uploaded_file = st.file_uploader("Upload a wav-file or a folder")



def main():

    if st.button("Register"):
        register_page()


if __name__ == "__main__":
    main()
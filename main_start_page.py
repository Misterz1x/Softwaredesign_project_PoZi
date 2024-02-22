from st_pages import Page, add_page_title, show_pages
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header




def register_page():
    st.title("Register Page")
    uploaded_file = st.file_uploader("Upload a wav-file or a folder")

def recognise_page():
    st.title("Recognise Page")
    uploaded_file = st.file_uploader("Upload a wav-file or a folder")
    if st.button("Activate Microphone"):
        #add recongnise code
        st.write("Wavecraft is listening")

def add_logo():
    logo_image = "crying_cat.jpg"
    st.image(logo_image, use_column_width=True)



def main():

    add_logo()

    st.title("Wavecraft")
    st.write("Welcome to Wavecraft! This website let you recognise your favorite songs and unknown musical pieces")

    if st.button("Register"):
        register_page()

    if st.button("Recognise"):
        recognise_page()

if __name__ == "__main__":
    main()
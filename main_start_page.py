from st_pages import Page, add_page_title, show_pages
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header





st.set_page_config( page_title="Wavecraft", page_icon=":musical_note:")



show_pages(
	[
		Page("register_page.py", "Upload your songs", "🎵"),
		Page("recognise_page.py", "Find the song", "🔮")
	]
)


#def register_page():
    #st.title("Register Page")
    #uploaded_file = st.file_uploader("Upload a wav-file or a folder")

#def recognise_page():
    #st.title("Recognise Page")
    #uploaded_file = st.file_uploader("Upload a wav-file or a folder")
    #if st.button("Activate Microphone"):
        #add recongnise code
        #st.write("Wavecraft is listening")

def add_logo():
    logo_image = "Pictures\crying_cat.jpg"
    st.image(logo_image, width=200)



def main():

    add_logo()

    st.title("Wavecraft")
    st.markdown("Welcome to Wavecraft! This website lets you recognise your favorite songs and unknown musical pieces")

if __name__ == "__main__":
    main()

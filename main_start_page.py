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

def add_logo():
	logo_image = "Pictures\Wavecraft_logo.png"
	st.image(logo_image, width=200)

def main():

	add_logo()

	st.title("Wavecraft")
	st.markdown("Welcome to Wavecraft! This website lets you recognise your favorite songs and unknown musical pieces")


if __name__ == "__main__":
	main()

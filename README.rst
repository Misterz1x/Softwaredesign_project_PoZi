Sound recognition and identification Programm
==============================
First tasks:
----------
* Install the setuptools package to be able to install the project with the setup.py file.
* Initialise the setup.py file to get nearly all necessary packages for the project.
* Create a basic structure for the project.
* Initialise a database to store the sound files and their features with the code:
python .\song_recogniser.py initialise
* Add a song to the database with the code:
python .\song_recogniser.py register <path_to_song>
* Recognise a song with the code:
python .\song_recogniser.py recognise <path_to_song>

------------------
22.02.2024:
Die Musikerkennung funktioniert mithilfe von Klassen und arbeitet objektorientiert.
* Es wird TinyDB verwendet, um die Songs und ihre Features zu speichern.
* Dementsprechend wird alles in eine JSON-Datei gespeichert.
* Erster Aufbau der Website
* Erster Aufbau der GUI

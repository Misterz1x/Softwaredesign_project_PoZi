Welcome to Wavecraft, your sound recognition and identification Programm!

## 1. Installation
For the installation of Wavecraft it would be the best to create a virtual invironment for python, called a venv. 
This is a clean environment for the programm to run in, without any other packages that could interfere with the programm. 
To create a venv, you first have to install the virtual invironment. You can use the following command in your terminal:

    'pip install virtualenv'

After that, you can create a venv with the following command:

    'python<version> -m venv <virtual-environment-name>'

For example:

    'mkdir projectA'
    'cd projectA'
    'python3.8 -m venv env'

After you created the venv, you can activate it with the following command (for windows):

    'venv\Scripts\activate'

Be sure to be in the right directory, where the venv is located.

After you activated the venv, you can install the required packages using the requirements.txt with the following command:

    'pip install -r requirements.txt'

After you installed the required packages, you can run the programm with the following command:
    
    'streamlit run .\main_start_page.py'

This will start the programm and open a new tab in your browser.

If you want to deactivate the venv, you can use the following command:

    'deactivate'

If you want to delete the venv, you can simply delete the folder, where the venv is located.



## 2. How to use Wavecraft
When you start the programm, you will see the start page of Wavecraft. Here you can choose between the different options of the programm.
On the left side you can see the navigation bar, where you can choose between the different options: 'Upload your songs' and 'Find your song'.
If you click on 'Upload your songs', there is the option to upload a songfile from your computer or to use a youtube link to a song. 
If you upload it from your computer you have to add the song titel and optionally the artist.
If you use the youtube link, the programm will download the song and analyze it.
If you click on 'Find your song', you can upload a song or record it with the microphone and the programm will then try to find the song in the database and show you the results.
If Wavecraft finds your song in the database, it will show you the song and the artist. You will be able to play the song and get addiditonal information about the song such as the bpm, the youtube thumpnail and graphs of the song.
On the right side you will see a database with the last found songs. 

## 3. How does Wavecraft work? 

Code-Structure explained using UML-Diagramm:
![Wavecraft UML-Diagramm]Softwaredesign_project_PoZi/Wavecraft_UML.png

## 4. Sources
The programm used the following sources:
https://github.com/notexactlyawe/abracadabra
https://github.com/scaperot/the-BPM-detector-python/blob/master/bpm_detection/bpm_detection.py
https://developers.google.com/youtube/v3/docs?hl=de

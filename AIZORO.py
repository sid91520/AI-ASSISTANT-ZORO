import speech_recognition as sr
import pyttsx3
import datetime
import os
from dateutil import parser
import re
import dateparser
import time
import threading
from googletrans import Translator
import random
import pygame
import requests
import wikipediaapi






# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
text_to_speech = pyttsx3.init()
text_to_speech.setProperty('rate', 170)
text_to_speech.setProperty('volume', 1.0) 
WETEHER_API_KEY = 'a5c751a33975b4af1a7b3ca28e6032be'
pygame.mixer.init()
available_songs = [
    {"title": "Lean On", "path": r'C:\Users\Admin\Music\lean-on.mp3'},
    {"title": "My heart will go on", "path": r'C:\Users\Admin\Music\my heart will go on.mp3'},
 ]
#dictionary to store tasks in the format:{task_name:task_description}
tasks={}

# Function to speak text
def speak(text):
    text_to_speech.say(text)
    text_to_speech.runAndWait()

# Function to listen to the user's voice
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source,timeout=5)
    
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your audio.")
        return ""
    except sr.RequestError as e:
        print("Sorry, an error occurred. {0}".format(e))
        return ""



# play music
def play_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()

# Function to pause music
def pause_music():
    pygame.mixer.music.pause()

# Function to resume music
def resume_music():
    pygame.mixer.music.unpause()

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()


def search_person_wikipedia(person_name):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(person_name)

    if page_py.exists():
        return page_py.text[:500]  # Limiting the response to the first 500 characters for brevity
    else:
        return f"Sorry, I couldn't find information about {person_name} on Wikipedia."


# Function to handle voice commands
def handle_command(command):
    if "hello" in command.lower():
        speak("Hello! How can I assist you today?")  
    elif "open notepad" in command.lower():
        os.system("notepad.exe")
        speak("What else i can do for you, say features to know other task")
    elif "open spotify" in command.lower():
        spotify_path = r"C:\Users\Admin\AppData\Roaming\Spotify\Spotify.exe"  # Replace with the actual path
        os.system(spotify_path)
        speak("What else can I do for you? Say 'features' to know other tasks.")

    elif "time" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("The current time is " + current_time)
        speak("What else i can do for you, say features to know other task")
    elif "features" in command.lower():
        speak("I have many features.I can Translate a language, open application, set task and even play games.")

#tasks asignmeet
    elif "add task" in command.lower():
        speak("Sure,give a title for the task you would like to add?")
        task_name = listen()
        if task_name:
            speak("please give a brief description of task description of the task?")
            task_description = listen()
            tasks[task_name] = task_description
            speak(f"Task '{task_name}' added.")

    elif "list of task" in command.lower():
        if tasks:
            speak("Here is a list of your tasks:")
            for task_name, task_description in tasks.items():
                speak(f"{task_name}: {task_description}")
        else:
            speak("You have no tasks.")
    elif "delete task" in command.lower():
        speak("Sure, what task would you like to delete?")
        task_name = listen()
        if task_name in tasks:
            del tasks[task_name]
            speak(f"Task '{task_name}' deleted.")
        else:
            speak("Task '{task_name}' does not exist.")
   

#translate my word   
    elif "translate" in command.lower():
        speak("Sure, what would you like to translate?")
        text_to_translate = listen()
        if text_to_translate:
            speak("What is the source language?")
            source_language = listen()
            speak("What is the target language?")
            target_language = listen()

            translator = Translator()
            translation = translator.translate(text_to_translate, src=source_language, dest=target_language)
            speak(f"The translation is: {translation.text}")
        else:
            speak("Please specify the text to translate.")

    # elif re.match(r"play music (.+)", command, re.IGNORECASE):
    #     match = re.match(r"play music (.+)", command, re.IGNORECASE)
    #     if match:
    #         song_name = match.group(1)
    #         # Replace 'path/to/your/song.mp3' with the actual path to your downloaded song
    #         music_path =r'C:\Users\Admin\Music\lean-on.mp3'
    #         play_music(music_path)
    #         speak(f"Now playing: {song_name}")
    #     else:
    #         speak("Please specify the song to play.")
# Handle music commands in the handle_command function
    elif re.match(r"play music", command, re.IGNORECASE):
        if available_songs:
        # Randomly select a song from the list
            selected_song = random.choice(available_songs)
            play_music(selected_song["path"])
            speak(f"Now playing: {selected_song['title']}")
        else:
            speak("There are no songs available.")


    elif "pause music" in command.lower():
        pause_music()
        speak("Music paused.")

    elif "resume music" in command.lower():
        resume_music()
        speak("Music resumed.")

    elif "stop music" in command.lower():
        stop_music()
        speak("Music stopped.")

    elif "weather" in command.lower():
        speak("Sure, please specify the city.")
        city = listen()

        if city:
            # Get weather information from OpenWeatherMap API
            weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WETEHER_API_KEY}"
            response = requests.get(weather_api_url)
            weather_data = response.json()

            if response.status_code == 200:
                description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']
                temperature_celsius = temperature - 273.15  # Convert temperature to Celsius

                speak(f"The weather in {city} is {description} with a temperature of {temperature_celsius:.2f} degrees Celsius.")
            else:
                speak("Sorry, I couldn't retrieve the weather information.")
    

    elif "search Wikipedia for" in command.lower():
        match = re.match(r"search Wikipedia for (.+)", command, re.IGNORECASE)
        if match:
            person_name = match.group(1)
            result = search_person_wikipedia(person_name)
            speak(result)
        else:
            speak("Please specify the person you want to search for on Wikipedia.")




    else:
        speak("I'm not sure how to respond to that.")
    

        # Main loop
if __name__ == "__main__":
    speak("Hello! I am your voice assistant zoro. How can i help you!")
   # open_notepad()
    
    while True:
        command = listen()
        if command:
            handle_command(command)

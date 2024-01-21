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
# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
text_to_speech = pyttsx3.init()


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
        audio = recognizer.listen(source,timeout=2)
    
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
    elif "exit" or "bye" or "close" in command.lower():
        speak("Goodbye!")
        exit()
    else:
        speak("I'm not sure how to respond to that.")




        # Main loop
if __name__ == "__main__":
    speak("Hello! I am your voice assistant zoro, luffys crew mate, how can i help you.")
   # open_notepad()
    
    while True:
        command = listen()
        if command:
            handle_command(command)

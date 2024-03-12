from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
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
import wikipedia
import logging
import webbrowser
import sys
import tkinter.messagebox as messagebox
import sqlite3

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
text_to_speech = pyttsx3.init()
text_to_speech.setProperty('rate', 130)
text_to_speech.setProperty('volume', 1.0)
WEATHER_API_KEY = 'a5c751a33975b4af1a7b3ca28e6032be'
pygame.mixer.init()
available_songs = [
    {"title": "lean on", "path": r'C:\Users\Admin\Documents\TYITPROJECT\musicfile\lean-on.mp3'},
    {"title": "my heart will go on", "path": r'C:\Users\Admin\Documents\TYITPROJECT\musicfile\my-heart-will-go-on.mp3'},
    {"title": "baby", "path": r'C:\Users\Admin\Documents\TYITPROJECT\musicfile\baby.mp3'},
    {"title": "beliver", "path": r'C:\Users\Admin\Documents\TYITPROJECT\musicfile\beliver.mp3'},
    {"title": "cheap thrills", "path": r'C:\Users\Admin\Documents\TYITPROJECT\musicfile\cheap-thrills.mp3'},
    {"title": "laal bindi", "path": r'C:\Users\Admin\Documents\TYITPROJECT\musicfile\laal-bindi.mp3'},
    {"title": "see you again", "path": r'C:\Users\Admin\Documents\TYITPROJECT\musicfile\see-you-again.mp3'}
]
# {task_name:task_description}
tasks = {}


def search_website(query, website):
    # Define the base URL for the website
    base_url = {
        "google": "https://www.google.com/search?q=",
        "stackoverflow": "https://stackoverflow.com/search?q=",
        # Add more websites as needed
    }
    if website.lower() in base_url:
        # Construct the search URL
        search_url = base_url[website.lower()] + query.replace(" ", "+")
        # Open the search URL in a web browser
        webbrowser.open(search_url)
        speak(f"Here are the search results for '{query}' on {website}.")
    else:
        speak("Sorry, I cannot search that website.")


# Function to speak text
def speak(text):
    text_to_speech.say(text)
    text_to_speech.runAndWait()


# Function to listen to the user's voice
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5)

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


def search_wikipedia(search_term):
    """
    Searches Wikipedia for a specific term.

    Args:
        search_term: The term to search for.

    Returns:
        A string containing the summary or an informative message.
    """
    try:
        summary = wikipedia.summary(search_term, sentences=2)  # Get summary with 2 sentences
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple possible results
        return f"Multiple matches found for '{search_term}'. Please specify further."
    except wikipedia.exceptions.PageError:
        # No information found
        return f"Sorry, I couldn't find information about '{search_term}' on Wikipedia."
    except Exception as e:
        # Unexpected error
        logging.error(f"Error searching Wikipedia: {e}")
        return "Something went wrong while searching Wikipedia. Please try again later."

def handle_command(command):
    response = None  # Initialize response to None
    if "hello" in command.lower():
        speak("Hello! How can I assist you today?")
        response = "Hello! How can I assist you today?"
    elif "open notepad" in command.lower():
        os.system("notepad.exe")
        speak("What else can I do for you? Say 'features' to know other tasks.")
        response = "What else can I do for you? Say 'features' to know other tasks."
    elif "open spotify" in command.lower():
        spotify_path = r"C:\Users\Admin\AppData\Roaming\Spotify\Spotify.exe"  # Replace with the actual path
        os.system(spotify_path)
        speak("What else can I do for you? Say 'features' to know other tasks.")
        response = "What else can I do for you? Say 'features' to know other tasks."
    elif "time" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("The current time is " + current_time)
        speak("What else can I do for you? Say 'features' to know other tasks.")
        response = f"The current time is {current_time}. What else can I do for you? Say 'features' to know other tasks."
    elif "features" in command.lower():
        speak("I have many features. like I can Translate a language, open applications, set task, do a web search and also search for people on google.")
        response = "I have many features. like I can Translate a language, open applications, set task, do a web search and also search for people on google."
    elif "add task" in command.lower():
        speak("Sure, give a title for the task you would like to add?")
        task_name = listen()
        if task_name:
            speak("Please give a brief description of the task.")
            task_description = listen()
            tasks[task_name] = task_description
            speak(f"Task '{task_name}' added.")
            response = f"Task '{task_name}' added."
        else:
            response = "Sorry, I couldn't understand the task name."
    elif "list of task" in command.lower():
        if tasks:
            speak("Here is a list of your tasks:")
            for task_name, task_description in tasks.items():
                speak(f"{task_name}: {task_description}")
            response = "Here is a list of your tasks."
        else:
            speak("You have no tasks.")
            response = "You have no tasks."
    elif "delete task" in command.lower():
        speak("Sure, what task would you like to delete?")
        task_name = listen()
        if task_name in tasks:
            del tasks[task_name]
            speak(f"Task '{task_name}' deleted.")
            response = f"Task '{task_name}' deleted."
        else:
            speak(f"Task '{task_name}' does not exist.")
            response = f"Task '{task_name}' does not exist."
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
            response = f"The translation is: {translation.text}"
        else:
            speak("Please specify the text to translate.")
            response = "Please specify the text to translate."
    # Add other command conditions here
    elif re.match(r"play music", command, re.IGNORECASE):
        if available_songs:
            # Randomly select a song from the list
            selected_song = random.choice(available_songs)
            play_music(selected_song["path"])
            speak(f"Now playing: {selected_song['title']}")
            response = f"Now playing: {selected_song['title']}"
        else:
            speak("There are no songs available.")
    elif "pause music" in command.lower():
        pause_music()
        speak("Music paused.")
        response="Music paused."

    elif "resume music" in command.lower():
        resume_music()
        speak("Music resumed.")
        response="Music resumed."

    elif "stop music" in command.lower():
        stop_music()
        speak("Music stopped.")
        response="Music stopped."

    elif "weather" in command.lower():
        speak("Sure, please specify the city.")
        city = listen()

        if city:
            # Get weather information from OpenWeatherMap API
            weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
            response = requests.get(weather_api_url)
            weather_data = response.json()

            if response.status_code == 200:
                description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']
                temperature_celsius = temperature - 273.15  # Convert temperature to Celsius

                speak(f"The weather in {city} is {description} with a temperature of {temperature_celsius:.2f} degrees Celsius.")
                response=f"The weather in {city} is {description} with a temperature of {temperature_celsius:.2f} degrees Celsius."
            else:
                speak("Sorry, I couldn't retrieve the weather information.")
    # wikipedia search    
    elif "search for" in command.lower():
        # Extract search term after "search for"
        search_term = command.lower().split("search for")[1].strip()
        # Perform Wikipedia search and provide feedback
        result = search_wikipedia(search_term)
        speak(result)
        response=result

    # browser open
    elif "search website" in command.lower():
        # Extract the query and website from the command
        match = re.match(r"search website (.+) for (.+)", command, re.IGNORECASE)
        if match:
            website = match.group(1).strip()
            query = match.group(2).strip()
            # Call the search_website function
            search_website(query, website)
            response=search_website
        else:
            speak("Please specify the website and the query.")
            response="Please specify the website and the query."
    elif "bye" or "close" in command.lower():
        if "bye" in command.lower() or "close" in command.lower():
            speak("Closing the assistant. Press speak to start again")
            response="Closing the assistant. Press speak to start again"
            sys.exit()  # Exit the program

    return response



class FeedbackForm:
    def __init__(self):
        self.root = Tk()
        self.root.title('Feedback Form')
        self.root.geometry('400x200')

        self.Email_label = Label(self.root, text='Email:')
        self.Email_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.Email_entry = Entry(self.root)
        self.Email_entry.grid(row=0, column=1, padx=5, pady=5)

        self.name_label = Label(self.root, text='Name:')
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.name_entry = Entry(self.root)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.feedback_label = Label(self.root, text='Feedback:')
        self.feedback_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.feedback_entry = Entry(self.root)
        self.feedback_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_button = Button(self.root, text='Submit', command=self.submit_feedback)
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.root.mainloop()

    def submit_feedback(self):
        name = self.name_entry.get()
        feedback = self.feedback_entry.get()
        email = self.Email_entry.get()




        if email and name and feedback:
            self.insert_feedback(email, name, feedback)
            messagebox.showinfo('Feedback Submitted', 'Thank you for your feedback!')
            self.root.destroy()
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def insert_feedback(self,email, name, feedback):
        conn = sqlite3.connect('feedback')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS feedback (email TEXT,name TEXT, feedback TEXT)')
        c.execute('INSERT INTO feedback VALUES (?, ?, ?)', (email, name, feedback))
        conn.commit()
        conn.close()



class Widget:
    def __init__(self):
        self.root = Tk()
        self.root.title('VOICE ASSISTANT ZORO')
        self.root.geometry('800x420')

        self.userFrame = LabelFrame(self.root,bg='black',fg='white',text='ZORO', font=('Railways', 26, 'bold'))
        self.userFrame.grid(row=0, column=0, padx=3, pady=3, sticky='nsew')

        self.conversationFrame = Frame(self.root)
        self.conversationFrame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        gif_path = r'C:\Users\Admin\Documents\TYITPROJECT\main project file\7kmF.gif'
        self.gif = Image.open(gif_path)
        self.animate_gif()

        btn = Button(self.root, text='Speak', font=('railways', 15, 'bold'), bg='#186F65', fg='white', command=self.start_voice_assistant)
        btn.grid(row=1, column=0, padx=3, pady=3)

        btn2 = Button(self.root, text='Close', font=('railways', 15, 'bold'), bg='white', fg='#7C73C0', command=self.show_feedback_form)
        btn2.grid(row=2, column=0, padx=3, pady=3)

        self.conversation_text = Text(self.conversationFrame, font=('Helvetica', 12), wrap='word')
        self.conversation_text.pack(fill='both', expand=True)


        self.root.mainloop()

        self.animate_thread = None

    def animate_gif(self):
        frames = [ImageTk.PhotoImage(frame.resize((730, 500))) for frame in ImageSequence.Iterator(self.gif)]
        self.gif_label = Label(self.userFrame, image=frames[0], bg='black')
        self.gif_label.grid(row=0, column=0, padx=10, pady=10)
        self.animate_gif_frames(frames)
        self.frames = frames  # Assuming frames are generated here

    def animate_gif_frames(self, frames):
        self.gif_idx = 0
        def update_frame():
            nonlocal frames
            frame = frames[self.gif_idx]
            self.gif_label.config(image=frame)
            self.gif_idx = (self.gif_idx + 1) % len(frames)
            self.root.after(100, update_frame)  # Schedule next update
        update_frame()  # Start the animation loop  

    def start_voice_assistant(self):
        speak("Hello! I am your voice assistant Zoro. How can I help you?")
        self.frames = self.animate_gif()  # Assuming animation generates frames

        # Define a function to continuously listen for commands
        def listen_for_commands():
            while True:
                command = listen()
                if command:
                    print(f"User: {command}")
                    response = handle_command(command)
                    print(f"Assistant: {response}")
                    self.conversation_text.insert(END, f"User: {command}\nAssistant: {response}\n\n")
                    self.conversation_text.see(END)  # Scroll to the bottom
        # Start listening for commands in a separate thread
        command_thread = threading.Thread(target=listen_for_commands)
        command_thread.start()
    def show_feedback_form(self):
        feedback_form = FeedbackForm()

if __name__ == "__main__":
    widget = Widget()




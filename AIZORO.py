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
import speedtest
from plyer import notification  #pip install plyer
from bs4 import BeautifulSoup
import pyautogui
from pynput.keyboard import Key, Controller
from time import sleep
# Initialize the speech recognition and text-to-speech engines
engine = pyttsx3.init() 
recognizer = sr.Recognizer()
text_to_speech = pyttsx3.init()
text_to_speech.setProperty('rate', 180)
text_to_speech.setProperty('volume', 1.0)
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)
WEATHER_API_KEY = 'a5c751a33975b4af1a7b3ca28e6032be'
NEWS_API_KEY = '2bc317281f5b4f19b54b6ad7dcad74d3'
pygame.mixer.init()
available_songs = [
    {"title": "lean on", "path": r'C:\Users\Siddharth\Documents\TYITPROJECT\musicfile\lean-on.mp3'},
    {"title": "my heart will go on", "path": r'C:\Users\Siddharth\Documents\TYITPROJECT\musicfile\my-heart-will-go-on.mp3'},
    {"title": "baby", "path": r'C:\Users\Siddharth\Documents\TYITPROJECT\musicfilebaby.mp3'},
    {"title": "beliver", "path": r'C:\Users\Siddharth\Documents\TYITPROJECT\musicfile\beliver.mp3'},
    {"title": "cheap thrills", "path": r'C:\Users\Siddharth\Documents\TYITPROJECT\musicfile\cheap-thrills.mp3'},
    {"title": "laal bindi", "path": r'C:\Users\Siddharth\Documents\TYITPROJECT\musicfile\laal-bindi.mp3'},
    {"title": "see you again", "path": r'C:\Users\Siddharth\Documents\TYITPROJECT\musicfile\see-you-again.mp3'}
]
# {task_name:task_description}
tasks = {}
keyboard = Controller()

def take_screenshot():
    current_directory = os.getcwd()
    screenshot_path = os.path.join(current_directory, "screenshot.jpg")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

def search_website(query, website):
    base_url = {
        "google": "https://www.google.com/search?q=",
        "stackoverflow": "https://stackoverflow.com/search?q=",
    }
    if website.lower() in base_url:
        search_url = base_url[website.lower()] + query.replace(" ", "+")
        webbrowser.open(search_url)
        speak(f"Here are the search results for '{query}' on {website}.")
    else:
        speak("Sorry, I cannot search that website.")


# Function to speak text
def speak(text):
    text_to_speech.say(text)
    text_to_speech.runAndWait()
def listen(prompt_message=None):
    if prompt_message:
        speak(prompt_message)
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


def fetch_news(topic):
    url = f'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': NEWS_API_KEY,
        'category': topic, 
        'language': 'en'

    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        if articles:
            headlines = [article['title'] for article in articles[:5]]  # Get top 5 headlines
            return headlines
        else:
            return ["No news available on this topic."]
    else:
        return ["Failed to fetch news. Please try again later."]


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
    elif "hello, how are you" in command.lower():
        speak("Hello! I'm fine, How can I assist you today?")
        response = "Hello! How can I assist you today?"
    elif "open notepad" in command.lower():
        os.system("notepad.exe")
        speak("opening notepad What else can I do for you?")
        response = "opening notepad What else can I do for you?"
    elif "open spotify" in command.lower():
        spotify_path = "Spotify.exe"  # Replace with the actual path
        os.system(spotify_path)
        speak("opening spotify What else can I do for you?")
        response = "Opening spotify. What else can I do for you?"
    elif "what is the time" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("The current time is " + current_time)
        speak("What else can I do for you? Say 'features' to know other tasks.")
        response = f"The current time is {current_time}. What else can I do for you? Say 'features' to know other tasks."
    elif "features" in command.lower():
        speak("I have many features. like I can Translate a language, open applications, set task, do a web search and also search for people on google.")
        response = "I have many features. like I can Translate a language, open applications, set task, do a web search and also search for people on google."
    
    elif "screenshot" in command.lower():
        take_screenshot()
        speak("Screenshot taken and saved in your main directory")
        response = "Screenshot taken and saved in your main directory"


    elif "pause" in command.lower():
        pyautogui.click(x=400, y=400)  # Adjust x and y values based on the actual coordinates
        speak("Video paused")
        response = "Video paused"

    elif "play" in command.lower():
        keyboard.press("k")
        speak("Video played")
        response = "Video played"
    elif "mute" in command.lower():
        keyboard.press("m")
        speak("Video muted")
        response = "Video muted"
    elif "volume up" in command.lower():
        volumeup()
        speak("Turning volume up, sir")
        response = "Turning volume up, sir"
    elif "volume down" in command.lower():
        volumedown()
        speak("Turning volume down, sir")
        response = "Turning volume down, sir"
    
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
    elif "search for" in command.lower():
        # Extract search term after "search for"
        search_term = command.lower().split("search for")[1].strip()
        # Perform Wikipedia search and provide feedback
        result = search_wikipedia(search_term)
        speak(result)
        response=result

    # browser open
    elif "search" in command:
        search_query = listen('What do you want to search for?')
        url = 'https://google.com/search?q=' + search_query
        webbrowser.get().open(url)
        speak('Here is what I found for ' + search_query)
        response = 'Performed a search for ' + search_query
        summary = search_wikipedia(search_query)
        if summary:
            speak(summary)
            response += "\nHere is some information about the search query:\n" + summary


    elif "tell me some news" in command.lower():
        speak("Sure, what type of news would you like to hear? For example, sports, politics, technology.")
        user_preference = listen().lower()
        news_headlines = fetch_news(user_preference)
        if news_headlines:
            speak("Here are the latest headlines:")
            for headline in news_headlines:
                speak(headline)
                response=headline
        else:
            speak("Sorry, I couldn't fetch the news at the moment.")
    
    elif "open youtube" in command.lower():
        search_query = command.lower().replace("openkkk youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.get().open(url)
        speak(f"{search_query}")
        response = f"{search_query}"


    elif "internet speed" in command.lower():
        try:
            wifi = speedtest.Speedtest()
            upload_net = wifi.upload() / 1048576  # Megabyte = 1024*1024 Bytes
            download_net = wifi.download() / 1048576
            response=("Wifi Upload Speed is", upload_net)
            response=("Wifi download speed is ", download_net)
            speak(f"Wifi download speed is {download_net} Megabytes per second.")
            speak(f"Wifi Upload speed is {upload_net} Megabytes per second.")
        except Exception as e:
            print("Error occurred while testing internet speed:", e)
            speak("Sorry, I couldn't test the internet speed at the moment. Please try again later.")

    
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

        self.conversationFrame = Frame(self.root,bg='blue')
        self.conversationFrame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        gif_path = r'C:\Users\Siddharth\Documents\TYITPROJECT\aiZoro.gif'
        self.gif = Image.open(gif_path)
        self.animate_gif()

        btn = Button(self.root, text='Speak', font=('railways', 15, 'bold'), bg='#186F65', fg='white', command=self.start_voice_assistant)
        btn.grid(row=1, column=0, padx=3, pady=3)

        btn2 = Button(self.root, text='Close', font=('railways', 15, 'bold'), bg='white', fg='#7C73C0', command=self.show_feedback_form)
        btn2.grid(row=2, column=0, padx=3, pady=3)

        self.conversation_text = Text(self.conversationFrame, font=('Helvetica', 10), wrap='word')
        self.conversation_text.pack(fill='both', expand=True)


        self.root.mainloop()

        self.animate_thread = None

    def animate_gif(self):
        frames = [ImageTk.PhotoImage(frame.resize((1000, 730))) for frame in ImageSequence.Iterator(self.gif)]
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

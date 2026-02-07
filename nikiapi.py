import random
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sys
import psutil
import time
import os
import pyautogui  # For screenshots
import pywhatkit  # For WhatsApp
import google.generativeai as genai

# --- 1. API Configuration ---
GEMINI_API_KEY = "AIzaSyCw3ClFkijyrJo-Z04MAod-GqWRe12p6KI" # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- 2. Voice Engine ---
def speak(text):
    print(f"Neek: {text}") 
    try:
        temp_engine = pyttsx3.init('sapi5') 
        voices = temp_engine.getProperty('voices')
        if voices:
            temp_engine.setProperty('voice', voices[0].id) 
        temp_engine.setProperty('rate', 175)
        temp_engine.say(text)
        temp_engine.runAndWait()
        temp_engine.stop() 
    except Exception as e:
        print(f"Voice Error: {e}")

# --- 3. AI Brain ---
def ask_gemini(prompt):
    try:
        full_prompt = f"You are Neek, a smart AI. Answer this in a mix of Hindi and English: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except:
        return "Sir, I'm having trouble connecting to my brain right now."

# --- 4. Greeting ---
def wishMe():
    hour = int(datetime.datetime.now().hour)
    greeting = "Good Morning!" if hour < 12 else "Good Afternoon!" if hour < 18 else "Good Evening!"
    speak(f"{greeting} I am Neek. System is fully loaded. What's the plan, Sir?")

# --- 5. Main Execution Loop ---
def process_commands():
    r = sr.Recognizer()
    r.energy_threshold = 400 
    r.dynamic_energy_threshold = True 

    with sr.Microphone() as source:
        print("[CALIBRATING...]")
        r.adjust_for_ambient_noise(source, duration=2)

    while True:
        with sr.Microphone() as source:
            print("\n>>> Listening...")
            r.pause_threshold = 0.8
            try:
                audio = r.listen(source, timeout=None, phrase_time_limit=8)
                print(">>> Processing...")
                query = r.recognize_google(audio, language='en-in').lower()
                print(f"User: {query}")
            except Exception:
                continue

        # --- 1. SYSTEM CONTROLS (OPEN/CLOSE) ---
        if 'open' in query:
            if 'chrome' in query:
                speak("Opening Chrome")
                os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe") # Adjust path if needed
            elif 'notepad' in query:
                speak("Opening Notepad")
                os.system("notepad.exe")
            elif 'youtube' in query:
                webbrowser.open("youtube.com")
            else:
                speak(f"Opening {query.replace('open', '')}")
                webbrowser.open(f"https://www.google.com/search?q={query}")

        elif 'close' in query:
            if 'chrome' in query:
                speak("Closing Chrome")
                os.system("taskkill /f /im chrome.exe")
            elif 'notepad' in query:
                speak("Closing Notepad")
                os.system("taskkill /f /im notepad.exe")
            elif 'browser' in query or 'edge' in query:
                os.system("taskkill /f /im msedge.exe")

        # --- 2. SCREENSHOT FEATURE ---
        elif 'screenshot' in query:
            speak("Taking screenshot, sir.")
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            name = f"screenshot_{timestamp}.png"
            img = pyautogui.screenshot()
            img.save(name)
            speak(f"Screenshot saved as {name}")

        # --- 3. WHATSAPP FEATURE ---
        elif 'send a message' in query or 'whatsapp' in query:
            try:
                speak("What should I say?")
                # We listen again for the message content
                with sr.Microphone() as source:
                    msg_audio = r.listen(source)
                    message = r.recognize_google(msg_audio)
                
                speak("Please tell me the phone number with country code.")
                with sr.Microphone() as source:
                    num_audio = r.listen(source)
                    number = r.recognize_google(num_audio).replace(" ", "")
                
                speak(f"Sending message to {number}")
                # This opens WhatsApp Web and sends the message
                pywhatkit.sendwhatmsg_instantly(f"+{number}", message)
                speak("Message delivered to the browser, sir.")
            except Exception as e:
                speak("I couldn't send the message. Please check the details.")

        # --- 4. UTILITIES ---
        elif 'battery' in query:
            speak(f"Sir, battery is at {psutil.sensors_battery().percent} percent.")

        elif 'stop' in query or 'exit' in query:
            speak("System offline. Goodbye sir.")
            sys.exit()

        # --- 5. AI RESPONSE (If no match above) ---
        else:
            ans = ask_gemini(query)
            speak(ans)

if __name__ == "__main__":
    wishMe()
    process_commands()
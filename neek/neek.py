
import random
import requests
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sys
import psutil
import time
import os
import pyautogui 
import pywhatkit 
import requests

# --- 1. Voice Engine ---
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

# --- 2. Helper for Listening (To prevent getting stuck) ---
def listen_to_user(r, source, message="Listening..."):
    try:
        print(f"\n>>> {message}")
        # timeout: wait 5 seconds to start speaking
        # phrase_time_limit: stop listening after 7 seconds of speaking
        audio = r.listen(source, timeout=5, phrase_time_limit=7)
        print(">>> Processing...")
        query = r.recognize_google(audio, language='en-in').lower()
        print(f"User: {query}")
        return query
    except sr.WaitTimeoutError:
        print(">>> No speech detected (Timeout).")
        return "none"
    except Exception:
        print(">>> Could not understand or connection error.")
        return "none"

# --- 3. Greeting ---
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12: 
        speak("Good Morning!")

    elif hour < 18: 
        speak("Good Afternoon!")   
    else: 
        speak("Good Evening!")  
    speak("Neek is online. Ready for your command.")


# --- 4. Main Logic Loop ---
def process_commands():
    r = sr.Recognizer()
    r.energy_threshold = 400 
    r.dynamic_energy_threshold = True 

    with sr.Microphone() as source:
        print("\n[CALIBRATING...] Please stay quiet...")
        r.adjust_for_ambient_noise(source, duration=2)
        print("[READY]")

        while True:
            query = listen_to_user(r, source)

            if query == "none":
                continue
            
            # --- CONVERSATION ---
            elif 'hello' in query or 'hi' in query:
                speak("Hello sir! I am listening.")
            
            elif 'kaise ho' in query or 'how are you' in query:
                speak(random.choice(["Main jhakaas hoon!", "I am fine sir, how about you?"]))
                

            elif 'kya kar rahe ho' in query or 'what are you doing' in query:
                speak("Bas sir, aapke system ki dekh-bhaal kar raha hoon aur aapke agle command ka wait kar raha hoon.")

            elif 'khana khaya' in query:
                speak("Sir main toh bijli aur data khaata hoon! Mere liye toh wahi dawat hai.")

            elif 'bor ho raha hun' in query or 'i am bored' in query:
                speak("Bore mat hoiye sir! Chaliye YouTube Shorts dekhte hain. Maje kijiye!")
                webbrowser.open("https://www.youtube.com/shorts/")

            elif 'kaun ho tum' in query or 'who are you' in query:
                speak("Main Neek hoon, aapka personal AI assistant. Main aapka kaam as" \
                "aan karne ke liye bana hoon.")


            elif 'battery' in query:
                battery = psutil.sensors_battery()
                speak(f"Battery is at {battery.percent} percent.")


            # --- WHATSAPP (The part that usually gets stuck) ---
            elif 'send a message' in query or 'whatsapp' in query:
                speak("Who is the receiver? Please say the number clearly.")
                # We reuse the same 'source' so we don't restart the mic
                phone_no = listen_to_user(r, source, "Waiting for Number...")
                phone_no = phone_no.replace(" 918487018865", "hello")
                
                if phone_no != "none":
                    speak("What is the message?")
                    message = listen_to_user(r, source, "Waiting for Message...")
                    # massag = r.listen(source, timeout=5, phrase_time_limit=7)

                    
                    if message != "none":
                        speak(f"Sending to {phone_no}")
                        # Note: pywhatkit takes 10 seconds to open the browser
                        pywhatkit.sendwhatmsg_instantly(f"+{phone_no}", message, wait_time=10)
                        speak("Message sent to browser.")
                else:
                    speak("I didn't get the number, cancelling.")

            # --- SCREENSHOT ---
            elif 'screenshot' in query:
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pyautogui.screenshot(f"snap_{ts}.png")
                speak("Screenshot saved.")

            # --- SYSTEM & SEARCH ---

            if 'create a file' in query or 'make a file' in query or 'write a note' in query:
                speak("Sir, what should be the name of the file?")
                filename = listen_to_user(r, source, "Say file name (e.g., 'notes')...")
                
                if filename != "none":
                    # Clean filename and add .txt extension
                    filename = filename.replace(" ", "_") + ".txt"
                    
                    speak(f"What should I write in {filename}?")
                    content = listen_to_user(r, source, "Say the content...")
                    
                    if content != "none":
                        try:
                            with open(filename, "w") as f:
                                f.write(content)
                            speak(f"File {filename} has been created successfully.")
                        except Exception as e:
                            speak("I couldn't create the file, there was an error.")
                    else:
                        speak("I didn't hear any content, cancelling file creation.")
                else:
                    speak("I didn't catch the filename, cancelling.")

            elif 'time' in query:
                speak(f"It's {datetime.datetime.now().strftime('%I:%M %p')}")

            elif 'open youtube' in query:
                webbrowser.open("youtube.com")
                

            elif 'open youtube' in query:
                speak("Opening YouTube")
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                speak("Opening Google")
                webbrowser.open("google.com")


            elif 'search google for' in query:
                topic = query.replace("search google for", "").strip()
                webbrowser.open(f"https://www.google.com/search?q={topic}")

            elif 'close this' in query or 'close window' in query or 'close that' in query:
                speak("Closing the current window, sir.")
                pyautogui.hotkey('alt', 'f4')
                
            elif 'close chrome' in query:
                os.system("taskkill /f /im chrome.exe")
            

            elif 'stop' in query or 'exit' in query:
                speak("Goodbye bro!")
                break
            
            else:
                # If nothing matches, just search google
                print("No command matched, searching web...")
                webbrowser.open(f"https://www.google.com/search?q={query}")

if __name__ == "__main__":
    wishMe()
    process_commands()


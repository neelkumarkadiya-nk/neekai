# Project Overview: Neek<br>
Neek is a Python-based AI Voice Assistant designed to function as a hands-free interface for a personal computer. By combining speech recognition, text-to-speech, and system automation, it allows users to manage digital tasks, retrieve information, and control system hardware through natural language.

ntelligent Automation: Handles tasks like sending WhatsApp messages, taking screenshots, and creating text files through voice commands.


System Control: Manages hardware and software, including checking battery levels, closing windows (Alt+F4), and terminating processes like Chrome.


Natural Interaction: Supports "Hinglish" (Hindi + English) conversational commands, making it more intuitive for Indian users.


Smart Search: Features a fail-safe mechanism that automatically performs a Google search if a specific command isn't recognized.

Tech Stack
Speech: SpeechRecognition (STT) & pyttsx3 (TTS).


Automation: PyAutoGUI & PyWhatKit.


System: psutil, os, & webbrowser.

import os
import speech_recognition as sr
import tkinter as tk
from threading import Thread
from langdetect import detect
import spacy

# Load the spaCy English model
nlp_en = spacy.load("en_core_web_sm")

# Create a Tkinter root window (this needs to be on the main thread)
root = tk.Tk()

def listen_and_print():
    recognizer = sr.Recognizer()

    # Make sure it uses your native FLAC binary
    os.environ["FLAC_CONVERTER"] = "/opt/homebrew/bin/flac"

    try:
        with sr.Microphone() as source:
            print("🎤 Say something... (press Ctrl+C to stop)")
            audio = recognizer.listen(source)

        print("⌛ Recognizing...")
        try:
            # Try recognizing speech in both English and Urdu
            text_en = recognizer.recognize_google(audio, language="en-US")
            text_ur = recognizer.recognize_google(audio, language="ur-PK")
            
            # Detect language
            text = text_en if detect(text_en) == 'en' else text_ur
            print("✅ You said:", text)

            # Now you can apply detect_intent function here
            detect_intent(text, detect(text))

        except sr.UnknownValueError:
            print("❌ Could not understand audio")
        except sr.RequestError as e:
            print(f"⚠️ Could not request results; {e}")

    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully. Bye!")

def detect_intent(text, language):
    print(f"Detecting intent for text: '{text}' in {language}")

    # Detect the intent based on the language
    if language == 'en':
        detect_intent_english(text)
    elif language == 'ur':
        detect_intent_urdu(text)

def detect_intent_english(text):
    print(f"Processing English text: '{text}'")
    
    # Use spaCy to process the English text
    doc = nlp_en(text.lower())  # Process text using spaCy

    # Intent detection with spaCy based on entity recognition and keywords
    if any(token.text in ["hello", "hi", "hey"] for token in doc):
        print("Intent detected: Greeting (English)")
    elif any(token.text in ["bye", "goodbye", "see you"] for token in doc):
        print("Intent detected: Farewell (English)")
    elif any(token.text in ["weather", "forecast"] for token in doc):
        print("Intent detected: Weather inquiry (English)")
    elif any(token.text in ["time", "clock"] for token in doc):
        print("Intent detected: Time inquiry (English)")
    else:
        print("Intent detected: Unknown (English)")

def detect_intent_urdu(text):
    print(f"Processing Urdu text: '{text[::-1]}'")
    if "ہیلو" in text:
        print("Intent detected: Greeting (Urdu)")
    elif "الوداع" in text:
        print("Intent detected: Farewell (Urdu)")
    elif "موسم" in text:
        print("Intent detected: Weather inquiry (Urdu)")
    elif "وقت" in text:
        print("Intent detected: Time inquiry (Urdu)")
    else:
        print("Intent detected: Unknown (Urdu)")

# Run the listen_and_print function in a separate thread to keep Tkinter on the main thread
def start_listening():
    listen_thread = Thread(target=listen_and_print)
    listen_thread.daemon = True  # Set the thread as a daemon thread
    listen_thread.start()

# Create and configure the GUI window
start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=20)

# Keep the window running
root.mainloop()

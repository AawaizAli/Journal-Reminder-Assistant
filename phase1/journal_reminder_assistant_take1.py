import os
import speech_recognition as sr
import tkinter as tk
from threading import Thread
from langdetect import detect
import spacy
from datetime import datetime
import parsedatetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import json

# Load only English spaCy model for now
nlp_en = spacy.load("en_core_web_sm")

# Remove the Urdu spaCy model loading
# Instead, use basic string operations for Urdu text processing
def process_urdu_text(text):
    """
    Basic Urdu text processing without spaCy
    Returns list of words
    """
    # Split on whitespace and remove empty strings
    return [word for word in text.split() if word.strip()]

# Initialize date/time parser
cal = parsedatetime.Calendar()

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Create root window
root = tk.Tk()
root.title("Journal & Reminder Assistant")

status_label = tk.Label(root, text="Ready", fg="black")
status_label.pack(pady=5)

# Store journal entries and reminders
journal_entries = []
reminders = []

def process_voice_input():
    """
    Captures voice input and processes it for both English and Urdu
    Returns the recognized text and detected language
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("🎤 Listening... (5 seconds)")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        print("⌛ Processing...")
        try:
            # Try English recognition first
            try:
                text_en = recognizer.recognize_google(audio, language="en-US")
                detected_lang = detect(text_en)
                
                # If detected as English, return English text
                if detected_lang == 'en':
                    print("Detected English speech")
                    return text_en, 'en'
                
            except (sr.UnknownValueError, Exception) as e:
                print(f"English recognition failed: {e}")
                
            # Try Urdu recognition
            try:
                text_ur = recognizer.recognize_google(audio, language="ur-PK")
                # Verify it contains Urdu characters
                if any('\u0600' <= c <= '\u06FF' for c in text_ur):
                    print("Detected Urdu speech")
                    return text_ur, 'ur'
                
            except (sr.UnknownValueError, Exception) as e:
                print(f"Urdu recognition failed: {e}")

            return None, None
            
        except sr.RequestError as e:
            print(f"⚠️ Error with the speech recognition service; {e}")
            return None, None
            
    except sr.WaitTimeoutError:
        print("⏰ Listening timed out. Please try again.")
        return None, None

def extract_datetime(text, language):
    """
    Extracts date and time information from the text
    Handles both English and Urdu date references
    """
    if language == 'en':
        time_struct, parse_status = cal.parse(text)
        if parse_status:
            return datetime(*time_struct[:6])
    else:
        # Basic Urdu date/time keywords mapping
        urdu_datetime_map = {
            'کل': 'tomorrow',
            'آج': 'today',
            'پرسوں': 'day after tomorrow'
            # Add more mappings as needed
        }
        for ur_word, en_word in urdu_datetime_map.items():
            if ur_word in text:
                time_struct, parse_status = cal.parse(en_word)
                if parse_status:
                    return datetime(*time_struct[:6])
    return None

def analyze_sentiment(text, language):
    """
    Analyzes the sentiment/emotion of the text
    Returns sentiment scores and emotion label
    """
    if language == 'en':
        # Use VADER for English
        scores = sentiment_analyzer.polarity_scores(text)
    else:
        # Enhanced Urdu sentiment analysis
        scores = {'compound': 0, 'pos': 0, 'neg': 0, 'neu': 0}
        
        # Expanded Urdu sentiment keywords
        positive_words = [
            'اچھا', 'خوش', 'بہترین', 'محبت', 'پیار', 'مزےدار', 
            'خوبصورت', 'زبردست', 'شاندار', 'کمال'
        ]
        negative_words = [
            'برا', 'غلط', 'ناراض', 'مایوس', 'دکھ', 'تکلیف', 
            'پریشان', 'بیمار', 'مشکل', 'غصہ'
        ]
        
        words = process_urdu_text(text)
        total_words = len(words)
        if total_words == 0:
            return scores

        pos_count = sum(1 for word in words if any(pos in word for pos in positive_words))
        neg_count = sum(1 for word in words if any(neg in word for neg in negative_words))
        
        scores['pos'] = pos_count / total_words
        scores['neg'] = neg_count / total_words
        scores['neu'] = (total_words - (pos_count + neg_count)) / total_words
        
        # Calculate compound score (-1 to 1)
        if pos_count + neg_count > 0:
            scores['compound'] = (pos_count - neg_count) / (pos_count + neg_count)
        
    # Determine emotion label with more granular thresholds
    if scores['compound'] >= 0.5:
        emotion = 'Very Positive'
    elif 0.1 <= scores['compound'] < 0.5:
        emotion = 'Positive'
    elif -0.1 < scores['compound'] < 0.1:
        emotion = 'Neutral'
    elif -0.5 <= scores['compound'] < -0.1:
        emotion = 'Negative'
    else:
        emotion = 'Very Negative'
    
    return scores, emotion

def add_journal_entry():
    """
    Records a journal entry with sentiment analysis
    """
    update_status("🎤 Listening...", "blue")
    text, lang = process_voice_input()
    
    if text:
        update_status("⌛ Processing...", "orange")
        scores, emotion = analyze_sentiment(text, lang)
        timestamp = datetime.now()
        
        entry = {
            'text': text,
            'language': lang,
            'timestamp': timestamp.isoformat(),
            'emotion': emotion,
            'sentiment_scores': scores
        }
        
        journal_entries.append(entry)
        save_data()
        
        feedback = f"Journal entry recorded. Detected emotion: {emotion}"
        speak_feedback(feedback, lang)
        update_status("✅ Entry recorded", "green")
    else:
        update_status("❌ Failed to record. Try again.", "red")

def add_reminder():
    """
    Sets a new reminder based on voice input
    """
    text, lang = process_voice_input()
    if text:
        datetime_obj = extract_datetime(text, lang)
        if datetime_obj:
            reminder = {
                'text': text,
                'language': lang,
                'datetime': datetime_obj.isoformat()
            }
            reminders.append(reminder)
            save_data()
            
            feedback = "Reminder set successfully"
            speak_feedback(feedback, lang)

def speak_feedback(text, language):
    """
    Converts text to speech for feedback
    """
    tts = gTTS(text=text, lang='en' if language == 'en' else 'ur')
    tts.save("feedback.mp3")
    os.system("start feedback.mp3")  # Adjust command based on OS

def save_data():
    """
    Saves journal entries and reminders to a JSON file
    """
    data = {
        'journal_entries': journal_entries,
        'reminders': reminders
    }
    with open('assistant_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_status(message, color="black"):
    status_label.config(text=message, fg=color)
    root.update()

# GUI Setup
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

journal_btn = tk.Button(frame, text="New Journal Entry", command=add_journal_entry)
journal_btn.pack(pady=5)

reminder_btn = tk.Button(frame, text="Set Reminder", command=add_reminder)
reminder_btn.pack(pady=5)

root.mainloop()
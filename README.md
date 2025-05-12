# **Urdu+English Voice-Based Journal & Reminder Assistant**

A voice-based assistant that helps users with journaling and reminders in both Urdu and English. The assistant allows users to log their moods, track their daily activities, and set reminders, all through natural language voice commands. The system uses speech recognition, natural language processing, emotion-aware summaries, and scheduling.

---

## **Features**

* **Multilingual Voice Input:** Supports voice commands in both Urdu and English.
* **Mood Logging:** Track your daily mood with natural language input, e.g., "Kal mood kaisa tha?" or "How was my mood yesterday?"
* **Emotion-Aware Summaries:** Provides emotional summaries based on the journal entry.
* **Reminder System:** Set reminders using voice commands, e.g., "Yaad dilana, raat 9 baje" (Remind me at 9 PM).
* **Scheduled Notifications:** Voice reminders delivered at the scheduled time.
* **Text-to-Speech (TTS):** Notifies the user about reminders and emotions via voice.

---

## **Technologies Used**

* **Python** – Main programming language.
* **SpeechRecognition** – For converting voice input to text.
* **spaCy** – NLP library for processing Urdu and English text.
* **Hugging Face Transformers** – For sentiment analysis and emotion-aware summaries.
* **APScheduler** – For scheduling reminders.
* **gTTS (Google Text-to-Speech)** – For generating voice reminders.
* **Parsedatetime** – For date/time extraction from natural language.

---

## **Installation**

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/urdu-english-voice-journal.git
cd urdu-english-voice-journal
```

### 2. Install dependencies:

Ensure you have **Python 3.6+** installed. Install the required packages using **pip**:

```bash
pip install -r requirements.txt
```

### 3. Set up the environment:

Make sure to have **Google Speech API** and **Google TTS API** keys configured if you're using the Google services for speech recognition and text-to-speech.

---

## **Usage**

1. **Start the assistant:**
   Run the following command to start the voice assistant:

   ```bash
   python assistant.py
   ```

2. **Voice Commands:**

   * **Log Mood:**
     *Example*: "Kal mood kaisa tha?" (How was my mood yesterday?)
   * **Log Journal Entry:**
     *Example*: "Mujhe aaj ka din kaise gaya?" (How was my day today?)
   * **Set Reminder:**
     *Example*: "Yaad dilana, raat 9 baje" (Remind me at 9 PM).

3. **Emotion-Aware Summary:**
   After logging a journal entry, the assistant provides a sentiment summary based on the text you entered.

---

## **Development Setup**

### 1. Speech Recognition Setup:

The assistant uses the **SpeechRecognition** library for voice-to-text conversion. You can use any microphone and configure your system for the best results.

```bash
pip install SpeechRecognition
```

* To recognize speech from the microphone, the assistant will capture your voice and convert it into text. This text is processed to understand your mood or to set a reminder.

### 2. NLP Processing:

The system uses **spaCy** and **Hugging Face** models to process natural language input, detect sentiments, and extract relevant information such as dates and times.

```bash
pip install spacy transformers
python -m spacy download en_core_web_sm
python -m spacy download xx_ent_wiki_sm
```

### 3. Setting up Reminders:

The assistant uses **APScheduler** to schedule reminders based on natural language input. You can customize the intervals and actions according to your needs.

```bash
pip install apscheduler
```

---

## **Contribution**

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

* **SpeechRecognition Library** for enabling voice input.
* **spaCy** for powerful NLP capabilities.
* **Hugging Face** for state-of-the-art pre-trained models.
* **APScheduler** for scheduling reminders and tasks.
* **Google TTS API** for converting text back into speech.

---

## **Future Improvements**

* Integration with cloud-based services for syncing data across devices.
* Support for more languages and dialects.
* Emotion-aware journaling with more advanced sentiment analysis.
* Integration with calendar services for better reminder management.


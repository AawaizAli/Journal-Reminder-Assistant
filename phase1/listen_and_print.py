import os
import speech_recognition as sr

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
            # text = recognizer.recognize_google(audio, language="ur-PK")
            text = recognizer.recognize_google(audio, language="en-US")
            print("✅ You said:", text)
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
        except sr.RequestError as e:
            print(f"⚠️ Could not request results; {e}")

    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully. Bye!")

listen_and_print()

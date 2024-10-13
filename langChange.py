import io
from gtts import gTTS # pip install gtts
import pygame # pip install pygame
import speech_recognition as sr # pip install SpeechRecognition
import pyttsx3 # pip install pyttsx3


# Initialize pyttsx3 
engine = pyttsx3.init()

# Initialize recognizer 
recognizer = sr.Recognizer()

# Function to take voice input and return recognized text
def voice_input():
    with sr.Microphone() as source:
        print("Listening!")
        engine.say("Listening!")
        engine.runAndWait()
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)
        print("Audio captured!")

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            # Recognize speech using Google's speech recognition
            if(text.lower() == "english"):
                language = "en"
            if(text.lower() == "arabic"):
                language = "ar"
            if(text.lower() == "spanish"):
                language = "es"
            if(text.lower() == "french"):
                language = "fr"
            if(text.lower() == "german"):
                language = "de"
            if(text.lower() == "russian"):
                language = "ru"
            else:
                language = "Not recognized"
            
            return language
        except sr.UnknownValueError:
            print("I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return None

def speak_text(lanuage, text):
    # Initialize gTTS object
    tts = gTTS(text, lang=lanuage)

    # Create a BytesIO object to hold the audio data
    with io.BytesIO() as audio_file:
        # Write the speech data to the file-like object
        tts.write_to_fp(audio_file)
        # Seek to the beginning of the BytesIO buffer so it can be read by pygame
        audio_file.seek(0)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        # Load the audio buffer into pygame
        pygame.mixer.music.load(audio_file, 'mp3')
        # Play the audio
        pygame.mixer.music.play()

        # Keep the script running until the audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# Main program
if __name__ == "__main__":
    lang = voice_input()  # Get voice input
    if lang != "Not recognized":
        speak_text(lang, "Hello, how are you?")  # Speak the recognized text
    else:
        print("I didn't catch that, could you repeat?")

    # if voice_input:
    #     speak_text(f"You said: {voice_input}")  # Speak the recognized text
    # else:
    #     speak_text("I didn't catch that, could you repeat?")

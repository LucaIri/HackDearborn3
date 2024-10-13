import io
from gtts import gTTS # pip install gtts
import pygame # pip install pygame
import speech_recognition as sr # pip install SpeechRecognition
import pyttsx3 # pip install pyttsx3
from translate import Translator #pip install translate




# Initialize pyttsx3 
engine = pyttsx3.init()

# Initialize recognizer 
recognizer = sr.Recognizer()


def translate_from_eng(text, language):
    print(language)
    translator = Translator(to_lang=language)
    output = translator.translate(text)
    print(output)
    return output

def find_first_word(text):
    words = text.split()
    if words:
        print (words[0])
        return words[0]
    else:
        return ""


# Function to take voice input and return recognized text
def voice_input():
    with sr.Microphone() as source:
        print("Pick a language. English, Spanish, French, Arabic, German, or Russian?")
        engine.say("Pick a language. English, Spanish, French, Arabic, German, or Russian?")
        engine.runAndWait()
        #recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)
        print("Audio captured!")

        try:
            print("Recognizing...")
            language = recognizer.recognize_google(audio)
            print(type(language)) 
            if(language.strip() == ""):
                print("TEST_HI")
                lang_abbrev = "en"
            else:
                language = find_first_word(language)
            print(language)
            # Recognize speech using Google's speech recognition
            if(language == "English"):
                print("HELLO")
                lang_abbrev = "en"
            elif(language == "Arabic"):
                lang_abbrev = "ar"
            elif(language == "Spanish"):
                lang_abbrev = "es"
            elif(language == "French"):
                lang_abbrev = "fr"
            elif(language == "German"):
                lang_abbrev = "de"
            elif(language == "Russian"):
                lang_abbrev = "ru"
           
            else:
                lang_abbrev = "Not recognized"
            
            return lang_abbrev
        except sr.UnknownValueError:
            print("I could not understand the audio.")
            # print("Please Try Again!")
            # engine.say("Please Try Again!")
            # engine.runAndWait()
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            # print("Please Try Again!")
            # engine.say("Please Try Again!")
            # engine.runAndWait()
        return "Not recognized"

def speak_text(lanuage, text):
    text = translate_from_eng(text, lanuage)
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
    lang_abb = voice_input()  # Get voice input
    if lang_abb != "Not recognized":
        speak_text(lang_abb, "Hello my friend")  # Speak the recognized text
    else:
        print("I didn't catch that, could you repeat?")

    # if voice_input:
    #     speak_text(f"You said: {voice_input}")  # Speak the recognized text
    # else:
    #     speak_text("I didn't catch that, could you repeat?")

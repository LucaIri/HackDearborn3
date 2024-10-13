import pyttsx3
import speech_recognition as sr
import pyaudio

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

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language="es-MX")
            # Recognize speech using Google's speech recognition
            # if(audio == "English"):
            #     text = recognizer.recognize_google(audio, language="en-US")
            # if(audio == "Arabic"):
            #     text = recognizer.recognize_google(audio, language="ar-SA")
            # if(audio == "Spanish"):
            #     text = recognizer.recognize_google(audio, language="es-MX")
            # if(audio == "French"):
            #     text = recognizer.recognize_google(audio, language="fr-FR")
            # if(audio == "German"):
            #     text = recognizer.recognize_google(audio, language="de-DE")
            # if(audio == "Russian"):
            #     text = recognizer.recognize_google(audio, language="ru")
            
            #text = recognizer.recognize_google(audio, language="ro-RO")
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return None

# Function to use pyttsx3 to speak the text
def speak_text(text):
    engine.setProperty()
    engine.say(text)
    engine.runAndWait()

# Main program
if __name__ == "__main__":
    voice_input = voice_input()  # Get voice input

    if voice_input:
        speak_text(f"You said: {voice_input}")  # Speak the recognized text
    else:
        speak_text("I didn't catch that, could you repeat?")

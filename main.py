
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import subprocess
import urllib.parse


# -------------------------------
# Initialize Voice Engine
# -------------------------------

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


# -------------------------------
# Text to Speech
# -------------------------------

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# -------------------------------
# Speech Recognition
# -------------------------------

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            print("Recognizing...")

            command = recognizer.recognize_google(audio)

            print("You:", command)

            return command.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I could not understand that.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""

        except Exception as e:
            print("Error:", e)
            return ""


# -------------------------------
# Tell Current Time
# -------------------------------

def tell_time():

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    speak("The current time is " + current_time)


# -------------------------------
# Tell Current Date
# -------------------------------

def tell_date():

    today = datetime.datetime.now().strftime("%d %B %Y")

    speak("Today's date is " + today)


# -------------------------------
# Wikipedia Search
# -------------------------------

def search_wikipedia(query):

    try:

        speak("Searching Wikipedia.")

        result = wikipedia.summary(
            query,
            sentences=2,
            auto_suggest=True
        )

        speak(result)

    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")

    except wikipedia.exceptions.PageError:
        speak("No Wikipedia page found.")

    except Exception:
        speak("Unable to search Wikipedia right now.")


# -------------------------------
# Weather Information
# -------------------------------

def get_weather(city):

    try:

        encoded_city = urllib.parse.quote(city)

        url = f"https://wttr.in/{encoded_city}?format=j1"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]

        result = (
            f"The weather in {city} is {description}. "
            f"Temperature is {temperature} degrees Celsius. "
            f"Humidity is {humidity} percent."
        )

        speak(result)

    except Exception as e:

        print("Weather error:", e)

        speak("Unable to fetch weather information.")


# -------------------------------
# Google Search
# -------------------------------

def google_search(query):

    speak("Searching Google.")

    search_url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )

    webbrowser.open(search_url)


# -------------------------------
# YouTube Search
# -------------------------------

def youtube_search(query):

    speak("Searching YouTube.")

    url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote(query)
    )

    webbrowser.open(url)


# -------------------------------
# Open System Applications
# -------------------------------

def open_application(command):

    if "notepad" in command:

        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad.")

    elif "calculator" in command:

        subprocess.Popen(["calc.exe"])
        speak("Opening Calculator.")

    elif "chrome" in command:

        webbrowser.open("https://www.google.com")
        speak("Opening Google Chrome or your default browser.")

    else:

        speak("Application not supported.")


# -------------------------------
# Process User Commands
# -------------------------------

def process_command(command):

    if not command:
        return True

    # Exit assistant
    if any(word in command for word in
           ["exit", "stop", "goodbye", "quit"]):

        speak("Goodbye! Have a nice day.")
        return False

    # Time
    elif "time" in command:

        tell_time()

    # Date
    elif "date" in command:

        tell_date()

    # Wikipedia
    elif "wikipedia" in command:

        query = command.replace("wikipedia", "").strip()

        if query:
            search_wikipedia(query)
        else:
            speak("Please tell me what to search on Wikipedia.")

    # Weather
    elif "weather" in command:

        city = command.replace("weather", "")
        city = city.replace("in", "").strip()

        if city:
            get_weather(city)
        else:
            speak("Please specify a city.")

    # YouTube
    elif "youtube" in command:

        query = command.replace("youtube", "").strip()

        if query:
            youtube_search(query)
        else:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")

    # Google Search
    elif "search" in command or "google" in command:

        query = command.replace("search", "")
        query = query.replace("google", "").strip()

        if query:
            google_search(query)
        else:
            speak("What would you like me to search?")

    # Open Applications
    elif "open" in command:

        open_application(command)

    # Greeting
    elif "hello" in command or "hi" in command:

        speak("Hello! How can I help you today?")

    # Unknown command
    else:

        speak("Sorry, I don't know how to perform that task.")

    return True


# -------------------------------
# Main Assistant
# -------------------------------

def main():

    speak("Hello! I am your personal voice assistant.")

    speak("You can ask me about time, date, weather, Wikipedia, or web search.")

    while True:

        command = listen()

        if command:

            if not process_command(command):
                break


# -------------------------------
# Program Entry Point
# -------------------------------

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        speak("Assistant stopped.")

    except Exception as e:

        print("Application Error:", e)
        speak("An unexpected error occurred.")

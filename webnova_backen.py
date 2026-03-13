import os
import subprocess
import webbrowser
import requests
import pyttsx3
import speech_recognition as sr
import pywhatkit as pkit
import psutil
import pyautogui
import pygetwindow as gw
import platform
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from ctypes import POINTER, cast
from pynput.keyboard import Controller
import threading
import time

# Optional audio control
try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    HAS_PYCAW = True
except ImportError:
    HAS_PYCAW = False

# Optional screen brightness control
try:
    import screen_brightness_control as sbc
    HAS_BRIGHTNESS = True
except ImportError:
    HAS_BRIGHTNESS = False

# ---------------------------
# Initialization
# ---------------------------
system = platform.system()

if system == "Windows":
    engine = pyttsx3.init("sapi5")
elif system == "Darwin":
    engine = pyttsx3.init("nsss")
else:
    engine = pyttsx3.init("espeak")

engine.setProperty('rate', 150)
keyboard = Controller()
volume_iface = None

if HAS_PYCAW:
    try:
        devices = AudioUtilities.GetSpeakers()
        iface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_iface = cast(iface, POINTER(IAudioEndpointVolume))
    except Exception:
        volume_iface = None

CURRENT_MODE = "chat"

# ---------------------------
# Speak Function
# ---------------------------
def speak(text: str):
    """Speak a text and print it"""
    print(f"[Nova] {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("[Speak error]", e)

# ---------------------------
# Speech Input Function
# ---------------------------
def listen_command(timeout=5) -> str:
    """Listen to microphone for commands"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = r.listen(source, timeout=timeout)
            command = r.recognize_google(audio)
            print(f"[Heard] {command}")
            return command
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            print("[Speech recognition error]", e)
            return ""

# ---------------------------
# Weather API
# ---------------------------
def get_weather(city: str) -> str:
    api_key = "YOUR_OPENWEATHER_API_KEY"
    if api_key == "YOUR_OPENWEATHER_API_KEY":
        return "Weather API key not set."
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()
        if str(data.get("cod")) != "404":
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {desc}."
        return "City not found."
    except:
        return "Unable to fetch weather."

# ---------------------------
# System Functions
# ---------------------------
def shutdown_pc():
    speak("Shutting down the PC in 10 seconds.")
    if system == "Windows":
        os.system("shutdown /s /t 10")
    else:
        os.system("shutdown -h now")

def plot_graph():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.title("Sine Graph")
    plt.show()
    speak("Plotting sine graph.")

def open_folder(folder_name):
    path = ""
    if "download" in folder_name:
        path = os.path.expanduser("~/Downloads")
    elif "documents" in folder_name:
        path = os.path.expanduser("~/Documents")
    if os.path.exists(path):
        if system == "Windows":
            os.startfile(path)
        else:
            subprocess.call(["open", path])
        speak(f"Opening {folder_name}")
        return "Folder opened"
    return "Folder not found"

def close_active_window():
    try:
        win = gw.getActiveWindow()
        if win:
            win.close()
            speak("Closed window")
            return "Window closed"
    except:
        return "Could not close window"

def close_youtube():
    closed = False
    for p in psutil.process_iter(attrs=['name']):
        if any(b in p.info['name'].lower() for b in ["chrome", "msedge", "firefox"]):
            p.kill()
            closed = True
    return "Browser closed" if closed else "Browser not found"

def increase_volume():
    if volume_iface:
        curr = volume_iface.GetMasterVolumeLevelScalar()
        volume_iface.SetMasterVolumeLevelScalar(min(curr + 0.1, 1.0), None)
        speak("Volume increased")
        return "Volume increased"
    return "Volume control unavailable"

def decrease_volume():
    if volume_iface:
        curr = volume_iface.GetMasterVolumeLevelScalar()
        volume_iface.SetMasterVolumeLevelScalar(max(curr - 0.1, 0.0), None)
        speak("Volume decreased")
        return "Volume decreased"
    return "Volume control unavailable"

# ---------------------------
# Alarm/Timer Function
# ---------------------------
alarms = []

def set_alarm(time_str):
    try:
        alarm_time = datetime.strptime(time_str, "%H:%M").time()
        alarms.append(alarm_time)
        threading.Thread(target=alarm_checker, args=(alarm_time,), daemon=True).start()
        speak(f"Alarm set for {time_str}")
        return f"Alarm set for {time_str}"
    except Exception as e:
        return f"Failed to set alarm: {e}"

def alarm_checker(alarm_time):
    while True:
        now = datetime.now().time()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            speak(f"Alarm ringing for {alarm_time.strftime('%H:%M')}!")
            break
        time.sleep(15)  # check every 15 seconds

# ---------------------------
# MAIN EXECUTION
# ---------------------------
def MainExecution(query: str):
    query = query.lower()

    # Speech command fallback
    if query.strip() == "":
        query = listen_command()

    # Greetings
    if "hello" in query:
        response = "Hello Ansh, I am Nova. How may I assist you?"
        speak(response)
        return response

    # Time
    elif "time" in query:
        response = f"The time is {datetime.now().strftime('%H:%M')}"
        speak(response)
        return response

    # Capital of India
    elif "capital of india" in query:
        response = "The capital of India is New Delhi."
        speak(response)
        return response

    # Shutdown
    elif "shutdown pc" in query:
        shutdown_pc()
        return "Shutting down PC"

    # Plot Graph
    elif "plot graph" in query:
        plot_graph()
        return "Graph plotted"

    # Open sites
    elif "open youtube" in query:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"
    elif "open google" in query:
        webbrowser.open("https://google.com")
        return "Opening Google"

    # Close YouTube/browser
    elif "close youtube" in query:
        return close_youtube()

    # Weather
    elif "weather" in query:
        weather = get_weather("Kanpur")
        speak(weather)
        return weather

    # Volume control
    elif "increase volume" in query:
        return increase_volume()
    elif "decrease volume" in query:
        return decrease_volume()

    # Move mouse
    elif "move mouse" in query:
        pyautogui.moveTo(500, 500)
        return "Mouse moved"

    # Alarm
    elif "set an alarm for" in query:
        time_str = query.split("set an alarm for")[-1].strip()
        return set_alarm(time_str)

    # Exit
    elif "exit" in query or "bye" in query:
        speak("Goodbye!")
        return "Goodbye!"

    # Unknown
    else:
        response = "I am not sure about that command."
        speak(response)
        return response

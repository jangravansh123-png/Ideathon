import tkinter as tk
import math
import time
import threading
import webbrowser
import os
import subprocess
import datetime

import speech_recognition as sr
import pyttsx3
import pyautogui


# =========================================================
# JARVIS CONFIG
# =========================================================

APP_NAME = "JARVIS"

BG = "#030609"
CYAN = "#00e5ff"
WHITE = "#ffffff"
GRAY = "#7d8b99"
GREEN = "#00ff9d"
RED = "#ff4d6d"


# =========================================================
# VOICE ENGINE
# =========================================================

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    """
    JARVIS speaks the given text.
    """

    update_status("SPEAKING")
    update_response(text)

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as error:
        print("TTS Error:", error)

    update_status("ONLINE")


# =========================================================
# SPEECH RECOGNITION
# =========================================================

recognizer = sr.Recognizer()


def listen():
    """
    Listen to microphone and convert speech to text.
    """

    update_status("LISTENING")

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.6
            )

            update_response("Listening...")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        update_status("THINKING")

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        update_response(f"You: {text}")

        return text.lower().strip()

    except sr.WaitTimeoutError:

        speak("I did not hear anything.")

    except sr.UnknownValueError:

        speak("Sorry, I could not understand that.")

    except sr.RequestError:

        speak("Speech recognition needs an internet connection.")

    except Exception as error:

        update_response(f"Microphone error: {error}")
        speak("There was a microphone problem.")

    return ""


# =========================================================
# COMPUTER ACTIONS
# =========================================================

def open_youtube():

    speak("Opening YouTube.")

    webbrowser.open(
        "https://www.youtube.com"
    )


def open_google():

    speak("Opening Google.")

    webbrowser.open(
        "https://www.google.com"
    )


def open_github():

    speak("Opening GitHub.")

    webbrowser.open(
        "https://github.com"
    )


def open_vscode():

    speak("Opening Visual Studio Code.")

    try:
        subprocess.Popen(
            ["code"]
        )

    except Exception:

        speak(
            "I could not find Visual Studio Code in the system path."
        )


def open_notepad():

    speak("Opening Notepad.")

    subprocess.Popen(
        ["notepad.exe"]
    )


def create_folder(name):

    name = name.strip()

    if not name:

        speak("Please tell me the folder name.")

        return

    # Remove characters that are unsafe for Windows filenames
    invalid = '<>:"/\\|?*'

    for char in invalid:
        name = name.replace(char, "")

    if not name:

        speak("That is not a valid folder name.")

        return

    path = os.path.join(
        os.getcwd(),
        name
    )

    if os.path.exists(path):

        speak(
            f"The folder {name} already exists."
        )

    else:

        os.makedirs(path)

        speak(
            f"Folder {name} created successfully."
        )


def type_text(text):

    text = text.strip()

    if not text:

        speak("Please tell me what I should type.")

        return

    speak("Typing your message.")

    time.sleep(1)

    pyautogui.write(
        text,
        interval=0.03
    )


# =========================================================
# COMMAND PROCESSOR
# =========================================================

def process_command(command):

    if not command:
        return

    command = command.lower().strip()

    # -----------------------------------------
    # YouTube
    # -----------------------------------------

    if "open youtube" in command:

        open_youtube()

    # -----------------------------------------
    # Google
    # -----------------------------------------

    elif "open google" in command:

        open_google()

    # -----------------------------------------
    # GitHub
    # -----------------------------------------

    elif "open github" in command:

        open_github()

    # -----------------------------------------
    # VS Code
    # -----------------------------------------

    elif (
        "open vs code" in command
        or "open visual studio code" in command
    ):

        open_vscode()

    # -----------------------------------------
    # Notepad
    # -----------------------------------------

    elif "open notepad" in command:

        open_notepad()

    # -----------------------------------------
    # Create folder
    # -----------------------------------------

    elif command.startswith("create folder"):

        folder_name = command[
            len("create folder"):
        ]

        create_folder(folder_name)

    # -----------------------------------------
    # Type text
    # -----------------------------------------

    elif command.startswith("type"):

        text = command[
            len("type"):
        ]

        type_text(text)

    # -----------------------------------------
    # Time
    # -----------------------------------------

    elif (
        "what is the time" in command
        or command == "time"
    ):

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak(
            f"The current time is {current_time}."
        )

    # -----------------------------------------
    # Date
    # -----------------------------------------

    elif (
        "what is the date" in command
        or command == "date"
    ):

        today = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak(
            f"Today is {today}."
        )

    # -----------------------------------------
    # Hello
    # -----------------------------------------

    elif (
        "hello jarvis" in command
        or command == "hello"
        or command == "hi"
    ):

        speak(
            "Hello. JARVIS is online and ready."
        )

    # -----------------------------------------
    # Status
    # -----------------------------------------

    elif (
        "status" in command
        or "are you online" in command
    ):

        speak(
            "All systems are online."
        )

    # -----------------------------------------
    # Exit
    # -----------------------------------------

    elif (
        command == "exit"
        or command == "quit"
        or command == "shutdown"
    ):

        speak(
            "JARVIS signing off."
        )

        root.after(
            1500,
            root.destroy
        )

    # -----------------------------------------
    # Unknown
    # -----------------------------------------

    else:

        speak(
            "I do not know that command yet."
        )


# =========================================================
# VOICE THREAD
# =========================================================

def start_listening():

    thread = threading.Thread(
        target=voice_worker,
        daemon=True
    )

    thread.start()


def voice_worker():

    command = listen()

    if command:

        process_command(command)


# =========================================================
# GUI
# =========================================================

root = tk.Tk()

root.title("JARVIS")

root.geometry(
    "900x700"
)

root.configure(
    bg=BG
)

root.resizable(
    False,
    False
)


canvas = tk.Canvas(
    root,
    width=900,
    height=700,
    bg=BG,
    highlightthickness=0
)

canvas.pack()


# =========================================================
# VARIABLES
# =========================================================

rotation = 0
pulse = 0
fps = 0

last_frame = time.perf_counter()
frame_counter = 0

status_text = "ONLINE"
response_text = "JARVIS is ready."


# =========================================================
# GUI UPDATE FUNCTIONS
# =========================================================

def update_status(text):

    global status_text

    status_text = text

    root.after(
        0,
        draw_interface
    )


def update_response(text):

    global response_text

    response_text = text

    root.after(
        0,
        draw_interface
    )


# =========================================================
# DRAW JARVIS
# =========================================================

def draw_interface():

    canvas.delete(
        "all"
    )

    cx = 450
    cy = 315

    # -----------------------------------------
    # Title
    # -----------------------------------------

    canvas.create_text(
        450,
        40,
        text="J A R V I S",
        fill=WHITE,
        font=("Segoe UI", 26, "bold")
    )

    canvas.create_text(
        450,
        72,
        text="PERSONAL AI ASSISTANT",
        fill=GRAY,
        font=("Segoe UI", 10)
    )

    # -----------------------------------------
    # Outer rotating rings
    # -----------------------------------------

    rings = [
        210,
        190,
        165,
        135
    ]

    for index, radius in enumerate(rings):

        canvas.create_oval(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            outline=CYAN,
            width=2
        )

    # -----------------------------------------
    # Rotating nodes
    # -----------------------------------------

    for i in range(18):

        angle = math.radians(
            rotation + i * 20
        )

        radius = 210

        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius

        canvas.create_oval(
            x - 4,
            y - 4,
            x + 4,
            y + 4,
            fill=CYAN,
            outline=""
        )

    # -----------------------------------------
    # Inner rotating nodes
    # -----------------------------------------

    for i in range(8):

        angle = math.radians(
            -rotation * 1.5 + i * 45
        )

        radius = 165

        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius

        canvas.create_oval(
            x - 3,
            y - 3,
            x + 3,
            y + 3,
            fill=GREEN,
            outline=""
        )

    # -----------------------------------------
    # Pulsing core
    # -----------------------------------------

    core_radius = (
        55
        + math.sin(pulse) * 8
    )

    canvas.create_oval(
        cx - core_radius,
        cy - core_radius,
        cx + core_radius,
        cy + core_radius,
        outline=CYAN,
        width=3
    )

    canvas.create_oval(
        cx - 35,
        cy - 35,
        cx + 35,
        cy + 35,
        fill=CYAN,
        outline=""
    )

    canvas.create_oval(
        cx - 20,
        cy - 20,
        cx + 20,
        cy + 20,
        fill=BG,
        outline=""
    )

    # -----------------------------------------
    # Status
    # -----------------------------------------

    canvas.create_text(
        450,
        535,
        text=status_text,
        fill=CYAN,
        font=("Segoe UI", 15, "bold")
    )

    # -----------------------------------------
    # Response
    # -----------------------------------------

    display_response = response_text

    if len(display_response) > 70:

        display_response = (
            display_response[:67] + "..."
        )

    canvas.create_text(
        450,
        570,
        text=display_response,
        fill=WHITE,
        font=("Segoe UI", 11)
    )

    # -----------------------------------------
    # FPS
    # -----------------------------------------

    canvas.create_text(
        25,
        675,
        anchor="w",
        text=f"FPS: {fps}",
        fill=GRAY,
        font=("Consolas", 10)
    )

    # -----------------------------------------
    # Microphone button
    # -----------------------------------------

    canvas.create_oval(
        405,
        610,
        495,
        670,
        outline=CYAN,
        width=2
    )

    canvas.create_text(
        450,
        640,
        text="🎙",
        fill=WHITE,
        font=("Segoe UI Emoji", 20)
    )


# =========================================================
# ANIMATION LOOP
# =========================================================

def animation_loop():

    global rotation
    global pulse
    global fps
    global frame_counter
    global last_frame

    rotation += 2
    pulse += 0.12

    frame_counter += 1

    now = time.perf_counter()

    if now - last_frame >= 1:

        fps = frame_counter

        frame_counter = 0
        last_frame = now

    draw_interface()

    root.after(
        16,
        animation_loop
    )


# =========================================================
# MOUSE CLICK
# =========================================================

def mouse_click(event):

    # Microphone button area

    if (
        400 <= event.x <= 500
        and 605 <= event.y <= 680
    ):

        start_listening()


canvas.bind(
    "<Button-1>",
    mouse_click
)


# =========================================================
# KEYBOARD SHORTCUT
# =========================================================

root.bind(
    "<space>",
    lambda event: start_listening()
)


# =========================================================
# START
# =========================================================

draw_interface()

animation_loop()

root.mainloop()
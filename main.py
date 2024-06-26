import pyperclip
import subprocess
import base64
import requests
from pynput import keyboard
import pyautogui
import datetime
import os


open_ai_key = ""
sysMes ="Du bist ein Politik und Wirtschaft Student und musst einen Test bestehen. Es sind multiple Choice Fragen und immer nur eine Antwort ist richtig!"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_directory = os.getcwd()
    filename = f"{current_directory}/folder/screenshot_{timestamp}.png"
    
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")
    return filename


def query_openai(base64_image, model, max_tokens=200):

    prompt = "Bitte schaue das Bild an. Beantworte die darin gestellte Frage. Es ist immer nur eine Antwort richtig. Wenn es keine Antwort-Möglichkeiten gibt, ist es eine Wahr oder Falsch Frage. Bitte antworte dann mit Wahr oder Falsch. Wenn es Antwortmöglichkeiten gibt, antworte mit der richtigen Antwortmöglichkeit und der Nummer. Bitte gebe keine Begründung an!\n"
    api_key = open_ai_key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages" : [
            {"role" : "system", "content" : sysMes},
            {"role" : "user", "content" : 
                [
                    {
                        "type" : "text",
                        "text": prompt
                    },
                    {
                        "type" : "image_url",
                        "image_url" : {
                            "url" : f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }   
        ]
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", 
        json=data, 
        headers=headers
    )

    return response.json()

def get_clipboard_content():
    try:
        text = pyperclip.paste()  # Attempts to paste clipboard content as text
        return text
    except Exception as e:
        return None

def send_notification(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def on_activate():

    print("Shortcut triggered!")

    filename = take_screenshot()
    base64_image = encode_image(filename)

    
    response = query_openai(base64_image=base64_image, model="gpt-4o")
    print(response)
    send_notification("Success", response["choices"][0]["message"]["content"])
    

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<shift>+o'),
    on_activate
)

with keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+o': on_activate
    }) as h:
    h.join()

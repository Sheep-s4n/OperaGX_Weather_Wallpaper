import requests
import json 
import subprocess
import time
from os import remove , listdir
from datetime import date
from pynput.keyboard import Key, Controller as KeyController
from pynput.mouse import Button, Controller as MouseController
from screeninfo import get_monitors
import pyperclip

with open('Data/settings.json', 'r') as json_file:
    settings = json.load(json_file)


CITY = settings['city']
API_KEY = settings['open-weather api key'] 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
MIN_TO_SEC = 60
HTTP_OK = 200
DATA_FILE = "Data/user_data.json"
startup_param = False 

monitors = get_monitors()
keyboard = KeyController()
mouse = MouseController()



def writeJSON(path, json) :
    with open(path, 'w') as json_file: 
        json_file.write(json)


def main(startup):

    def click_left(position):
        mouse.position = position
        mouse.press(Button.left)
        mouse.release(Button.left)

    # Get weather data
    response = requests.get(URL)

    if response.status_code == HTTP_OK:
        data = response.json()
        
        # Retrieve theme URL
        weather = data['weather'][0]['description']
        weather_list = list(settings['themes'].keys())

        print(f"Weather for {settings['city']} is {weather}")

        find_match = False

        for desc in weather_list:
            if desc == weather:
                find_match = True
                break

        if not find_match:
            if "clouds" in weather:
                weather = "broken clouds"
            for desc in weather_list:
                if desc in weather:
                    weather = desc 

        wallpaper_url = settings['themes'][weather]

        path = settings["themes files path"]
        themes = listdir(path)
        url_parts = wallpaper_url.rstrip('/').split('/')
        new_theme_name = url_parts[-1] if url_parts else None
        

        if wallpaper_url == "":
            print(f"No wallpaper set for {weather}")
            print("Ending program...")
            exit(0)

        print(f"Found matching wallpaper: {wallpaper_url}")


        # avoid running the script if the wallpaper choosen is already set
        if len(themes) == 1:
            current_theme_name = themes[0][:-4]
            if current_theme_name == new_theme_name:
                writeJSON(DATA_FILE , 
f'''{{
    "last_weather": "{weather}",
    "last_updated": "{f"{date.today()}/{time.strftime('%H:%M:%S' , time.localtime())}"}",
    "last_wallpaper": "{wallpaper_url}",
    "last_theme": "{new_theme_name}"
}}''') 
                print("Wallpaper is already set, skipping...")
                return


        # Remove all current walpapers from PC 

        for theme in themes:
            remove(f'{path}/{theme}')

        # Open new OperaGX window
        subprocess.Popen([settings["opera launcher path"] ,"--new-window" ,wallpaper_url])

        # Wait for webpage to load 
        if startup:
            time.sleep(float(settings['url loading timeout startup']))
        else:
            time.sleep(float(settings['url loading timeout']))

        # Calculate mouse position
        first_monitor_width = monitors[0].width
        first_monitor_height = monitors[0].height

        default_mouse_pos = (
        first_monitor_width - (first_monitor_width / 6) if settings["cursor X"] == "default" else int(settings["cursor X"] ), 
        first_monitor_height / 2 if settings["cursor Y"] == "default" else int(settings["cursor Y"])
        )
        
        click_left(default_mouse_pos)

        # Open the console window
        keyboard.press(Key.ctrl_l)
        keyboard.press(Key.shift_l)
        keyboard.tap("j")
        keyboard.release(Key.shift_l)
        keyboard.release(Key.ctrl_l)

        time.sleep(2)


        click_left(default_mouse_pos)

        # Inject script to download the wallpaper 

        script = open("inject.js", "r")
        content = script.read().replace("\n", "")
        if settings["copy script on clipboard"] == "True":
            clipboard_content = pyperclip.paste()
            pyperclip.copy(content)
            keyboard.press(Key.ctrl_l)
            keyboard.tap("v")
            keyboard.release(Key.ctrl_l)
        else:
            keyboard.type(content)
        
        keyboard.tap(Key.enter)

        time.sleep(float(settings['closing window timeout']))

        # Close operaGX window
        keyboard.press(Key.ctrl_l)
        keyboard.tap("w")
        keyboard.release(Key.ctrl_l)

        # setting back old clipboard content
        if settings["copy script on clipboard"] == "True":
            pyperclip.copy(clipboard_content)

        writeJSON(DATA_FILE , 
f'''{{
    "last_weather": "{weather}",
    "last_updated": "{f"{date.today()}/{time.strftime('%H:%M:%S' , time.localtime())}"}",
    "last_wallpaper": "{wallpaper_url}",
    "last_theme": "{new_theme_name}"
}}''') 

    else:
        print("Request to OpenWeather API failed")
        print("Tip: check your api key")


# Main function called here
if "startup" in settings["mode"]: 
    subprocess.Popen(settings["opera launcher path"])
    startup_param = True

if "repeat" in settings["mode"]:
    while True:
        main(startup_param)
        startup_param = False 
        print(f"Waiting for {settings['repeat interval']} minutes...")
        time.sleep(float(settings["repeat interval"]) * MIN_TO_SEC)
        # reload the file for any changes
        with open('Data/settings.json', 'r') as json_file:
            settings = json.load(json_file)
else:
    main(startup_param)

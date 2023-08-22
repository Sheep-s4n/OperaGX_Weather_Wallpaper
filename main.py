import requests
import json 
import subprocess
import time
from os import remove , listdir
from pynput.keyboard import Key, Controller as KeyController
from pynput.mouse import Button, Controller as MouseController
from screeninfo import get_monitors


with open('settings.json', 'r') as json_file:
    settings = json.load(json_file)

CITY = settings['city']
API_KEY = settings['open-weather api key'] 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
MIN_TO_SEC = 60
HTTP_OK = 200

monitors = get_monitors()
keyboard = KeyController()
mouse = MouseController()

# Remove all current walpapers from PC 
path = settings["themes files path"]
themes = listdir(path)

for theme in themes:
    remove(f'{path}/{theme}')


def main():
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

        if wallpaper_url == "":
            print(f"No wallpaper set for {weather}")
            print("Ending program...")
            exit(0)

        print(f"Found matching wallpaper: {wallpaper_url}")

        # Open new OperaGX window
        process = subprocess.Popen([settings["opera launcher path"] ,"--new-window" ,wallpaper_url])

        # Wait for webpage to load 
        time.sleep(int(settings['url loading timeout']))

        # Open the console window
        keyboard.press(Key.ctrl_l)
        keyboard.press(Key.shift_l)
        keyboard.tap("j")
        keyboard.release(Key.shift_l)
        keyboard.release(Key.ctrl_l)

        time.sleep(int(settings['url loading timeout']))

        # Calculate mouse position
        first_monitor_width = monitors[0].width
        first_monitor_height = monitors[0].height

        default_mouse_pos = (
        first_monitor_width - (first_monitor_width / 6) if settings["mouse pos width"] == "default" else int(settings["mouse pos width"] ), 
        first_monitor_height / 2 if settings["mouse pos height"] == "default" else int(settings["mouse pos height"])
        )

        # Set mouse position and click
        mouse.position = default_mouse_pos
        mouse.press(Button.left)
        mouse.release(Button.left)

        # Inject script to download the wallpaper 

        script = open("inject.js", "r")
        content = script.read().replace("\n", "")
        keyboard.type(content)
        keyboard.tap(Key.enter)

        time.sleep(int(settings['closing window timeout']))

        # Close operaGX window
        keyboard.press(Key.ctrl_l)
        keyboard.tap("w")
        keyboard.release(Key.ctrl_l)

    else:
        print("Request to OpenWeather API failed")
        print("Tip: check your api key")


# Main function called here
if "startup" in settings["mode"]: 
    process = subprocess.Popen(settings["opera launcher path"])

if "repeat" in settings["mode"]:
    while True:
        main()
        time.sleep(int(settings["repeat interval"]) * MIN_TO_SEC)
        # reload the file for any changes
        with open('settings.json', 'r') as json_file:
            settings = json.load(json_file)
else:
    main()

#none
#startup 
#repeat
#startup-repeat
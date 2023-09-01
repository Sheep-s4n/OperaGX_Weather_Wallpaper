import requests
import json 
import subprocess
import time
import random
from os import remove , listdir
import datetime
from pynput.keyboard import Key, Controller as KeyController
from pynput.mouse import Button, Controller as MouseController
from screeninfo import get_monitors
import pyperclip
import socket
from dragonfly import Window


with open('Data/settings.json', 'r') as json_file:
    settings = json.load(json_file)


CITY = settings['city']
API_KEY = settings['open-weather api key'] 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
MIN_TO_SEC = 60
HTTP_OK = 200
DATA_FILE = "Data/user_data.json"

monitors = get_monitors()
keyboard = KeyController()
mouse = MouseController()

def has_internet_connection():
    try:
        # Try to create a socket connection to a well-known server (Google's DNS server)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        pass
    return False
    
def is_OperaGXOpen():
    return len(Window.get_matching_windows("opera.exe")) > 0

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def handleTimeWallpaper():
    if 'time_overwrite' in settings['themes']:
        wallpaper = getWallpaper(settings["themes"], "time_overwrite")
        if wallpaper : print("Overwritting wallpaper with time dependent wallpaper")
        return wallpaper
    else:
        return False

def getWallpaper(object , key):
    wallpaper = object[key]
    if isinstance(wallpaper, dict):
        current_time = datetime.time( time.localtime().tm_hour ,  time.localtime().tm_min)
        start_hour, start_min = map(int, object[key]["start-time"].split(":"))
        start_time = datetime.time(start_hour , start_min)
        end_hour, end_min = map(int, object[key]["end-time"].split(":"))
        end_hour = 0 if end_hour == 24 and end_min == 0 else end_hour
        end_time = datetime.time(end_hour , end_min)
        if time_in_range(start_time , end_time , current_time):
            wallpaper = object[key]["wallpaper"]
        else: 
            return False
    if isinstance(wallpaper , list):
        # check if dict
        has_time_wallpaper=False
        for url in wallpaper:
           if isinstance(url , dict):
                has_time_wallpaper = True
                break
        if has_time_wallpaper:
            # generator expression
            # {what to return} for {element name} in {list} if {condition for returning}
            for i , wallpp in enumerate(wallpaper):
                if not isinstance(wallpp, dict): continue
                wallpaper_res = getWallpaper(object[key] , i)
                # wallpaper is a valid time wallpaper
                if wallpaper_res: return wallpaper_res
        
        # current time is not on any wallpaper time range
        no_time_wallpapers = [url for url in wallpaper if isinstance(url, str)]
        # no other wallpapers
        if len(no_time_wallpapers) == 0: return False
        index = random.randint(0, len(no_time_wallpapers) - 1)
        wallpaper = no_time_wallpapers[index]
    return wallpaper



def writeJSON(path, json) :
    with open(path, 'w') as json_file: 
        json_file.write(json)

def click_left(position):
    mouse.position = position
    mouse.press(Button.left)
    mouse.release(Button.left)

# Calculate mouse position
first_monitor_width = monitors[0].width
first_monitor_height = monitors[0].height

default_mouse_pos = (
first_monitor_width - (first_monitor_width / 6) if settings["cursor X"] == "default" else int(settings["cursor X"] ), 
first_monitor_height / 2 if settings["cursor Y"] == "default" else int(settings["cursor Y"])
)

def InjectScript(content):
    
    click_left(default_mouse_pos)

    if settings["copy script on clipboard"] == "True":
        pyperclip.copy(content)
        keyboard.press(Key.ctrl_l)
        keyboard.tap("v")
        keyboard.release(Key.ctrl_l)
    else:
        keyboard.type(content)
    
    keyboard.tap(Key.enter)



def main():

    if not has_internet_connection():
        print("You don't have an active internet connection")
        print("Couldn't make a request to openWeather API servers")                
        print("Closing function...")
        return

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
                    break
        
        def switchToDefaultWallpaper():
            print(f"No wallpaper matches for {weather} at {time.strftime('%H:%M' , time.localtime())}")
            print("Switching to default wallpaper")
            wallpaper_url = getWallpaper(settings["themes"] , "default")
            if not wallpaper_url:
                print(f"No default wallpaper found for {time.strftime('%H:%M' , time.localtime())}")
                print("Closing function...")
                return False
            else:
                return wallpaper_url

        wallpaper_url = handleTimeWallpaper()
        if not wallpaper_url:
            if weather in settings["themes"]:
                wallpaper_url = getWallpaper(settings["themes"] , weather)
                if not wallpaper_url:
                    wallpaper_url = switchToDefaultWallpaper()
                    # no default wallpaper
                    if not wallpaper_url:
                        return
            else:
                wallpaper_url = switchToDefaultWallpaper()
                # no default wallpaper
                if not wallpaper_url:
                    return

        path = settings["themes files path"]
        themes = listdir(path)
        url_parts = wallpaper_url.rstrip('/').split('/')
        new_theme_name = url_parts[-1] if url_parts else None
        
        print(f"Found matching wallpaper: {wallpaper_url}")


        # avoid running the script if the wallpaper choosen is already set
        if len(themes) == 1:
            current_theme_name = themes[0][:-4]
            if current_theme_name == new_theme_name:
                writeJSON(DATA_FILE , 
f'''{{
    "last_weather": "{weather}",
    "last_updated": "{f"{datetime.date.today()}/{time.strftime('%H:%M:%S' , time.localtime())}"}",
    "last_wallpaper": "{wallpaper_url}",
    "last_theme": "{new_theme_name}"
}}''') 
                print("Wallpaper is already set, skipping...")
                if not is_OperaGXOpen():
                    subprocess.Popen(settings["opera launcher path"])
                return


        # Remove all current walpapers from PC 

        for theme in themes:
            remove(f'{path}/{theme}')

        is_startup = False
        if not is_OperaGXOpen():
            subprocess.Popen(settings["opera launcher path"])
            time.sleep(0.5)
            is_startup = True
        # Open new OperaGX window
        subprocess.Popen([settings["opera launcher path"] ,"--new-window" ,wallpaper_url])
        
        # Wait for webpage to load 
        if is_startup:
            time.sleep(float(settings['open OperaGX delay']))
        else:
            time.sleep(float(settings['url loading delay']))

        click_left(default_mouse_pos)
        click_left(default_mouse_pos)

        # Open the console window
        keyboard.press(Key.ctrl_l)
        keyboard.press(Key.shift_l)
        keyboard.tap("j")
        keyboard.release(Key.shift_l)
        keyboard.release(Key.ctrl_l)

        OperaWindowCount = len(Window.get_matching_windows("opera.exe")) - 1 # window is already opened
        

        # Inject script to download the wallpaper 

        script = open("inject.js", "r")
        content = script.read().replace("\n", "")
        clipboard_content = pyperclip.paste()

        iteration_count = 0
        max_iterations = float(settings['url loading delay']) + 10
        InjectScript(content)
        while len(Window.get_matching_windows("opera.exe")) != OperaWindowCount: # looping script execution until the windows is closed
                if iteration_count >= max_iterations:
                    print("Failed to inject script")
                    return 
                InjectScript(content)
                time.sleep(1)
                iteration_count += 1
        
        if settings["copy script on clipboard"] == "True":
            pyperclip.copy(clipboard_content)

        writeJSON(DATA_FILE , 
f'''{{
    "last_weather": "{weather}",
    "last_updated": "{f"{datetime.date.today()}/{time.strftime('%H:%M:%S' , time.localtime())}"}",
    "last_wallpaper": "{wallpaper_url}",
    "last_theme": "{new_theme_name}"
}}''') 

    else:
        print("Couldn't find weather description")
        data = response.json()
        print(f"Error ({data['cod']}): {data['message']}")


if "repeat" in settings["mode"]:
    while "repeat" in settings["mode"]:
        main()
        print(f"Waiting for {settings['repeat interval']} minutes...")
        time.sleep(float(settings["repeat interval"]) * MIN_TO_SEC)
        # reload the file for any changes
        with open('Data/settings.json', 'r') as json_file:
            settings = json.load(json_file)
else:
    main()

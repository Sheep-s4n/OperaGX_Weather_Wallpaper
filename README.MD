# OperaGX Weather Wallpaper 

# Description
**OperaGX Weather Wallpaper** is a simple python script made to change your `OperaGX` based on the current weather of the city you provided.It only works with [OperaGX official website](https://addons.opera.com/en/wallpapers) wallpapers.

## How it works
1. The script deletes all your current wallpaper (save them in another folder if you don't want to lose them).
2. It finds the weather for the city you provided using the [OpenWeather API](https://openweathermap.org/api).
3. It gets the wallpaper that matches the weather for the city.
4. The script launches the wallpaper link in a new `operaGX` window .
5. It downloads the new wallpaper using a script injected in chrome/chromium dev tools (that's the only way I found to run `javascript` code on [addons.opera.com](https://addons.opera.com/) as chrome extensions do not work on this subdomain for security reasons).
6. The script closes the window and the new wallpaper is set shortly after.

# Prerequisites
You must have [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/cli/pip_download/) installed on your computer to run the script (and `OperaGX` of course).

# Installation and Usage
## 1. Code downloading
In order to use the script, you have to run the `git` command:
```
git clone https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper.git
```
Or, you can download it manually:

![download github code example](https://i.ibb.co/PxTNd4W/image.png)
## 2. Dependencies downloading
Run this `pip` command to install all requires dependencies:
```
pip install -r requirements.txt
```
## 3. Setting up the options
Options for running the script are located in **[settings.json](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/Data/settings.json)**.
### Settings explanation:

- **`open-weather api key`** : your [key](https://home.openweathermap.org/api_keys) for the OpenWeather API.

- **`city`** : city used to get weather.

- **`opera launcher path`** : `operaGX` *launcher.exe* path.

- **`themes files path`** : `OperaGX` wallpaper files path.

- **`url loading timeout`** : seconds to wait for the web page to be fully loaded (increment if you're browsing on a potato computer).

- **`closing window timeout`** : seconds to wait for the `javascript` code to run.

- **`cursor X`** : default is `"default"` , change it if the cursor doesn't land on the chrome dev tool console (usually for multiple monitor computer).

- **`cursor Y`** : same as `mouse pos width` but for height.

-  **`copy script on clipboard`** : the value is "True" or "False". Copy the `javascript` code on clipboard so as to run it much faster.

- **`themes`** : choose which theme to apply for each weather condition.

- **`mode`** : there are 3 modes:
	- `"startup"` : in this mode you use the **[main.py](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/main.py)** as your `operaGX` launcher, and each time you launch `operaGX` using it,it sets the wallpaper.
    - `"repeat"` : this mode runs the script infinitely until you send a `SIGINT` to the program by typing `ctrl+c`.
    - `"startup-repeat"` this mode combines the two other modes into a single one.

- **`repeat interval`** : Only for `"repeat"` and `"startup-repeat"` modes, defines the number of minutes until the next wallpaper is set.

- **`url loading timeout startup`** : Only for `"startup"` mode, defines the number of seconds to wait for `OperaGX` to start up (because `OperaGX` usually takes longer to start up the first time).

## 4. Running the script
Now you just have to run the python script using `python`:
```
python main.py
```
Or, using the newer version, `python3`
```
python3 main.py
```
Alternatively, you can use the **[launch_daemon.vbs](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/launch_daemon.vbs)** file in windows the launch the script in the background

⚠️ **Important: [inject.js](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/inject.js) and [Data](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/tree/main/Data) have to be in the same folder as **[main.py](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/main.py)** in order to run the script without any issues.** ⚠️
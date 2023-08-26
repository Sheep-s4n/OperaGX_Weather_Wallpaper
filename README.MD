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

[![download github code example](https://i.ibb.co/PxTNd4W/image.png)](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/archive/refs/heads/main.zip)
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

- **`url loading delay`** : seconds to wait for the web page to be fully loaded (increment if you're browsing on a potato computer).

- **`open OperaGX delay`** : seconds to wait for OperaGX to start up (increment if you're browsing on a potato computer).

- **`cursor X`** : default is `"default"` , change it if the cursor doesn't land on the chrome dev tool console (usually for multiple monitor computer).

- **`cursor Y`** : same as `mouse pos width` but for height.

-  **`copy script on clipboard`** : the value is "True" or "False". Copy the `javascript` code on clipboard so as to run it much faster.

- **`themes`** : choose which theme to apply for each weather condition provided by the the `OpenWeather` API. **For example:**
  ```
  "themes" : {
      "snow":"https://addons.opera.com/en/wallpapers/details/in-the-snow-anime/"
  }
  ```

  This code will set the `https://addons.opera.com/en/wallpapers/details/in-the-snow-anime/` wallpaper when the weather description is `snow`.

  **You can also set multiple wallpaper for a single weather description such as in the following code:**
  ```
  "scattered clouds":["https://addons.opera.com/en/wallpapers/details/summer/", "https://addons.opera.com/en/wallpapers/details/windmill-anime/"]
  ```
  In this case the wallpaper will be randomly chosen.

  **Moreover, you can set a time-dependent wallpaper for a weather description:**
  ```
  "few clouds":[
      {
          "start-time": "19:00",
          "end-time": "21:00",
          "wallpaper" :"https://addons.opera.com/en/wallpapers/details/anime-girl-looking-at-sunset/"
      }
  ]
  ```  
  In this code snippet, the wallpaper will be `"https://addons.opera.com/en/wallpapers/details/anime-girl-looking-at-sunset/"` between `19:00` and `20:00` for the weather description `few clouds`
    
    **Furthermore, you can set a time-dependent wallpaper that will be set regardless of the weather in the `time_overwrite` section:**
  ```
  "time_overwrite" : {
  	"start-time": "20:30",
  	"end-time": "24:00",
  	"wallpaper" : "https://addons.opera.com/en/wallpapers/details/endless-galaxy-train/"
  },
  ```
  The `https://addons.opera.com/en/wallpapers/details/anime-girl-looking-at-sunset/` will bet set from `19:00` to `24:00` (same as `00:00`) no matter what weather it is.
  
  **Finally, you can combine multiple options, as shown in the following example:**
  ```
  "few clouds":[
      {
          "start-time": "19:00",
          "end-time": "21:00",
          "wallpaper" :["https://addons.opera.com/en/wallpapers/details/anime-girl-looking-at-sunset/","https://addons.opera.com/en/wallpapers/details/silhouette-sunset-mountains/"]
      },"https://addons.opera.com/en/wallpapers/details/time-alone/"
  ]
  ```
  Here, the wallpaper will be chosen randomly between `https://addons.opera.com/en/wallpapers/details/anime-girl-looking-at-sunset/` and `https://addons.opera.com/en/wallpapers/details/silhouette-sunset-mountains/` from `19:00` to `21:00` and the rest of the time it will be `https://addons.opera.com/en/wallpapers/details/time-alone/`

	**If no wallpaper is found the default wallpaper will be used. You can set the `default` wallpaper like this:**
    ```
	"default":"https://addons.opera.com/en/wallpapers/details/coding-den-live-wallpaper/"
    ```
	Weather descriptions are sorted in such a way that the weather placed highest in the `JSON` object takes priority over the others. **For example, if the weather is `thunderstorm with rain` the `rain` wallpaper will be the one chosen in the following example as `rain` wallpaper is higher in the object than the `thunderstorm` wallpaper:**
    ```
    "rain":"https://addons.opera.com/en/wallpapers/details/rainy-day-future-city/",
    "thunderstorm":"https://addons.opera.com/en/wallpapers/details/sasuke/"
    ```
	**You can also add a new key-value pair to the object for specific cases as `thunderstorm with rain`:**
    ```
    "thunderstorm with rain":"https://addons.opera.com/en/wallpapers/details/old-steves-pub/"
    ```

- **`mode`** : there is one mode for the moment:
    - `repeat` : this mode runs the script infinitely until you send a `SIGINT` to the program by typing `ctrl+c`.
   
- **`repeat interval`** : only for `repeat` mode, defines the number of minutes until the next wallpaper is set.

## 4. Running the script
Now you just have to run the python script using `python`:
```
python main.py
```
Or, using the newer version, `python3`:
```
python3 main.py
```
Alternatively, you can use the **[launch_daemon.vbs](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/launch_daemon.vbs)** file in windows the launch the script in the background. In order to close the daemon process, you have  to run the **[stop_daemon.vbs](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/stop_daemon.vbs)** script (or just close the `python.exe` process from task manager).

⚠️ **Important: [inject.js](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/inject.js) and [Data](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/tree/main/Data) have to be in the same folder as **[main.py](https://github.com/Sheep-s4n/OperaGX_Weather_Wallpaper/blob/main/main.py)** in order to run the script without any issues.** ⚠️
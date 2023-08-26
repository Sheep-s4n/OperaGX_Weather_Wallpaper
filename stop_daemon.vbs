Dim oShell : Set oShell = CreateObject("WScript.Shell")
oShell.Run "taskkill /im python.exe /f", , True



  Furthermore, you can set a time-dependent wallpaper that will be set regardless of the weather in the `time_overwrite` section:
  ```
  "time_overwrite" : {
  	"start-time": "20:30",
  	"end-time": "24:00",
  	"wallpaper" : "https://addons.opera.com/en/wallpapers/details/endless-galaxy-train/"
  },
  ```
  The `https://addons.opera.com/en/wallpapers/details/anime-girl-looking-at-sunset/` will bet set from `19:00` to `24:00` (same as `00:00`) no matter what weather it is.
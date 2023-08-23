Dim oShell : Set oShell = CreateObject("WScript.Shell")
oShell.Run "taskkill /im python.exe /f", , True


Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c python main.py"
oShell.Run strArgs, 0, false
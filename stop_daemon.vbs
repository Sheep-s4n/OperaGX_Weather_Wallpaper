Dim oShell : Set oShell = CreateObject("WScript.Shell")
oShell.Run "taskkill /im python.exe /f", , True
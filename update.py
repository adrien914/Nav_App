import requests

try:
    print("Updating Window.exe ...")
    r = requests.get("https://github.com/adrien914/Nav_App/raw/master/Nav_App/Window.exe")

    content = r.content

    with open("Window.exe", "wb") as file:
        file.write(r.content)
        print("Update complete !")
except Exception as e:
    print(str(e))
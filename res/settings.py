import os, json

globalSettings = {}

def initSettings():
    defaultSettings = {
        # UI Settings
        "theme": "light",
        "uiScaling": 1.0,
        "-":"-",
        # File Path Settings
        "pathToPlayerList": "/data/playerList.json",
        "--":"--",
        # Timer Settings
        "timerMinutes": 2,
        "timerSeconds": 30,
        "timerEnabled": True
    }
    global globalSettings
    globalSettings = defaultSettings.copy()

def checkSettingsExist():
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    return os.path.exists(parentDir + "/data/settings.json")

def writeFile():
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    
    with open(parentDir + "/data/settings.json", 'w') as f:
        json.dump(globalSettings,f,indent=2,ensure_ascii=False)
        f.close()

def loadSettings():
    if checkSettingsExist():
        pass
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    
    with open(parentDir + "/data/settings.json", 'r') as f:
        global globalSettings
        globalSettings = json.load(f)
        f.close()

def main():

    
if __name__ == "__main__":
    main()
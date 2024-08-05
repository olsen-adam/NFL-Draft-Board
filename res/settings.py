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

def writeFile():
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    
    with open(parentDir + "/data/settings.json", 'w') as f:
        json.dump(globalSettings,f,indent=2,ensure_ascii=False)
        f.close()

def main():
    initSettings()
    writeFile()
    
if __name__ == "__main__":
    main()
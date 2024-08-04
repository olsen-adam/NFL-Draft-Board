import os

globalSettings = {}

def __init__():
    defaultSettings = {
        # UI Settings
        "theme": "light",
        "uiScaling": 1.0,
        
        # File Path Settings
        "pathToPlayerList": "data/playerList.json",
        "pathToSettingsList": "data/settings.json",
        
        # Timer Settings
        "timerMinutes": 2,
        "timerSeconds": 30,
        "timerEnabled": True
    }
    globalSettings = defaultSettings.copy()

def writeFile():
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    
    
    # with open(, 'w') as f:

def main():
    writeFile()
    
if __name__ == "__main__":
    main()
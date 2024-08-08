import os, json

globalSettings = {}
defaultSettings = {}

def getDefaultSettings():
    """Sets the default settings for the settings file.
    """
    
    global defaultSettings
    defaultSettings = {
        # UI Settings
        "theme": "dark",
        "uiScaling": 1.0,
        "isFullscreen": True,
        "lastWidth": 700,
        "lastHeight": 500,
        # File Path Settings
        "pathToPlayerList": "/data/playerList.json",
        # Timer Settings
        "timerMinutes": 2,
        "timerSeconds": 30,
        "timerEnabled": True,
        # Player Settings
        "numPlayers": 10,
        "numRounds": 16,
        "tradesEnabled": False
    }

def writeFile():
    """Writes the global settings to the settings file.
    """
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    
    with open(parentDir + "/data/settings.json", 'w') as f:
        json.dump(globalSettings,f,indent=2,ensure_ascii=False)
        f.close()

def regenSettings():
    """Regenerates the settings file with the default settings and writes it to the file.
    """
    
    getDefaultSettings()
    global globalSettings
    globalSettings = defaultSettings.copy()
    writeFile()

def checkSettingsExist():
    """Checks if the settings file exists.

    Returns:
        Boolean: If the settings file exists or not
    """
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    return os.path.exists(parentDir + "/data/settings.json")

def loadSetting(settingName: str):
    """Loads a setting from the settings file.

    Args:
        settingName (str): The name of the setting to load

    Returns:
        any: The value of the setting loaded from the settings file
    """
    
    if not checkSettingsExist():
        regenSettings()
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    
    with open(parentDir + "/data/settings.json", 'r') as f:
        allSettings = json.load(f)
        f.close()
        try: 
            assert settingName in allSettings, "Setting does not exist."
            return allSettings[settingName]
        except Exception as e:
            print(f"Error with loading the setting \"{settingName}\", {e}")
            return None

def loadRootPath():
    """Loads the root path of the project.

    Returns:
        str: The root path of the project
    """
    
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    return parentDir

def loadAllSettings():
    """Load all settings from the settings file.

    Returns:
        dict: a dictionary of all settings in the settings file
    """
    
    if not checkSettingsExist():
        regenSettings()
    
    currDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
    
    with open(parentDir + "/data/settings.json", 'r') as f:
        allSettings = json.load(f)
        f.close()
        return allSettings

def setSetting(settingName: str, settingValue):
    """Set a setting to a new value.

    Args:
        settingName (str): the name of the setting to set
        settingValue (_type_): the value to set the setting to

    Returns:
        Boolean: Whether the setting was set successfully
    """
    
    if not checkSettingsExist():
        regenSettings()
    global globalSettings
    globalSettings = loadAllSettings()
    try:
        assert settingName in globalSettings, "Setting not found."
        assert type(globalSettings[settingName]) == type(settingValue), "Setting type mismatch."
        globalSettings[settingName] = settingValue
        writeFile()
        return True
    except Exception as e:
        print(f"Error with setting the setting \"{settingName}\" to ({settingValue}), {e}")
        return False

def setAllSettings(newSettings: dict):
    """Set all settings to the new settings provided.

    Args:
        newSettings (dict): a dictionary of settings to set

    Returns:
        Boolean: Whether the settings were set successfully
    """
    if not checkSettingsExist():
        regenSettings()
    
    try :
        global globalSettings
        globalSettings = loadAllSettings()
        for setting in newSettings:
            setSetting(setting, newSettings[setting])
        writeFile()
        return True
    except Exception as e:
        print(f"Error with setting the settings to {newSettings}, {e}")
        return False

def main():
    print("Scaling:",loadSetting("uiScaling"))
    print("Nothing:", loadSetting("nothing"))
    # print("All Settings:", loadAllSettings())
    # print("Set Test - True :", setSetting("uiScaling", 2))
    # print("New Scaling:",loadSetting("uiScaling"))
    # print("Set Test - False:", setSetting("balls", 1.5))
if __name__ == "__main__":
    main()
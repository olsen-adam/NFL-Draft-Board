import requests, json, datetime
from .settings import *

DEBUG = False

def writeData():
    """Writes the data from the NFL API to a json file. It will also add a field to the json file to keep track of when the file was last updated.
    """
    if DEBUG: print("Retriving Data...")
    url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerList"
    headers = {
     	"x-rapidapi-key": "a2fb693d31msh972917021b87f4bp13ce74jsn44791cd6dd35",
		"x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
	}

    response = requests.get(url, headers=headers)
    data = response.json()
    currDate = datetime.datetime.timestamp(datetime.datetime.now())
	
    # TODO: Check the settings file for the path to the playerList.json file
    fileLocation = loadRootPath() + loadSetting("pathToPlayerList")
    jsonFile = open(fileLocation, "w")

	# Add a field to see when the last time that the file was updated
    data["currdate"] = currDate

    json.dump(data, jsonFile, ensure_ascii=False, indent=4)
    jsonFile.close()
    print("Data has been written to the file sucessfully.")

def checkFile(seconds=0, minutes=0, hours=12):
    """Using the timestamp from the json file, this function will check if the file is older than the specified time. If it is, it will return True, otherwise it will return False.

    Args:
        seconds (int, optional): The seconds value before the file needs refreshing. Defaults to 0.
        minutes (int, optional): The minutes value before the file needs refreshing. Defaults to 0.
        hours (int, optional): The hours value before the file needs refreshing. Defaults to 12.

    Returns:
        Boolean: If the file needs refreshing, it will return True, otherwise it will return False.
    """
    dataNeedsRefreshing = False
    totalSeconds = (hours*60*60) + (minutes*60) + seconds
    try:
        fileLocation = loadRootPath() + loadSetting("pathToPlayerList")
        with open(fileLocation,"r") as json_file:
            data = json.load(json_file)
            oldDate = data["currdate"]
            diff = abs((datetime.datetime.fromtimestamp(oldDate) - datetime.datetime.now()).total_seconds())
            if DEBUG: print(f"Total Seconds: {totalSeconds}\nOld Date: {oldDate}\nDifference: {diff}")
            dataNeedsRefreshing = diff >= totalSeconds
    except Exception as e:
        dataNeedsRefreshing = True
    return dataNeedsRefreshing

def refreshAPI(seconds=0, minutes=0, hours=12):
    """Check if the file needs refreshing. If it does, it will write the data to the json file.

    Args:
        seconds (int, optional): The amount of seconds between JSON updates. Defaults to 0.
        minutes (int, optional): The amount of minutes between JSON updates. Defaults to 0.
        hours (int, optional): The amount of hours between JSON updates. Defaults to 12.
    """
    if checkFile(seconds,minutes,hours): writeData()

def main():
    shouldGetData = checkFile()
    if shouldGetData: writeData()
    
if __name__ == "__main__":
    main()
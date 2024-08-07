import requests, json, datetime
import settings

DEBUG = False

def writeData():
    print("Retriving Data...")
    url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerList"
    headers = {
     	"x-rapidapi-key": "a2fb693d31msh972917021b87f4bp13ce74jsn44791cd6dd35",
		"x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
	}

    response = requests.get(url, headers=headers)
    data = response.json()
    currDate = datetime.datetime.timestamp(datetime.datetime.now())
	
    # TODO: Check the settings file for the path to the playerList.json file
    fileLocation = settings.loadRootPath() + settings.loadSetting("pathToPlayerList")
    jsonFile = open(fileLocation, "w")

	# Add a field to see when the last time that the file was updated
    data["currdate"] = currDate

    json.dump(data, jsonFile, ensure_ascii=False, indent=4)
    jsonFile.close()

def checkFile(seconds=0, minutes=0, hours=12):
    dataNeedsRefreshing = False
    totalSeconds = (hours*60*60) + (minutes*60) + seconds
    try:
        fileLocation = settings.loadRootPath() + settings.loadSetting("pathToPlayerList")
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
    if checkFile(seconds,minutes,hours): writeData()

def main():
    shouldGetData = checkFile()
    if shouldGetData: writeData()
    
if __name__ == "__main__":
    main()
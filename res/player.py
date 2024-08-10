import PIL.Image
import json, PIL, os, requests, io
class Player:
    def __init__(self, data: dict):
        self.data = data
        self.name = self.data["cbsName"]
        self.espnHeadshot = self.data["espnHeadshot"]
        self.id = self.data["id"]
        self.photo = self.getHeadshotTransparent()
        if self.photo is None:
            # Image does not exist/failed to load, so load default image
            currDir = os.path.dirname(os.path.abspath(__file__))
            parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
            self.photo = PIL.Image.open(parentDir + "/data/missing.jpg")
        
    def getHeadshotTransparent(self):
        """getHeadshotTransparent - Get the headshot of the player with a transparent background

        Returns:
            Image: Image from ESPN with a transparent background, None if failed to load
        """
        response = requests.get(self.espnHeadshot)
        try:
            if response.status_code == 200:
                imageData = io.BytesIO(response.content)
                regImage = PIL.Image.open(imageData)
                return regImage
            else:
                return None
        except Exception as e:
            return None
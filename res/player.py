import PIL.Image
import json, PIL, os, requests, io
class Player:
    def __init__(self, data: dict):
        self.data = data
        self.name = self.data.get("espnName")
        self.id = self.data.get("espnID")
        self.espnHeadshot = self.data.get("espnHeadshot")
        self.position = self.data.get("pos")
        self.colour = self.setColour()
        
    def getHeadshotTransparent(self):
        """getHeadshotTransparent - Get the headshot of the player with a transparent background

        Returns:
            Image: Image from ESPN with a transparent background, None if failed to load
        """
        response = requests.get(self.espnHeadshot)
            
        currDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.abspath(os.path.join(currDir, os.pardir))
        defaultPhoto = PIL.Image.open(parentDir + "/data/missing.jpg")
            
        try:
            if response.status_code == 200:
                imageData = io.BytesIO(response.content)
                regImage = PIL.Image.open(imageData)
                return regImage
            else:
                return defaultPhoto
        except Exception as e:
            return defaultPhoto
        
    def setColour(self):
        """Simple function that uses a hash function to generate a colour based on the pos
        """
        pos = "%-2s" % self.position
        a = ord(pos[0])
        b = ord(pos[1])
        minVal = min(a,b) + 10
        
        num1 = max(((a * b) % 255),minVal)
        hex1 = str(hex(num1)).lstrip("0x")
        num2 = max(((abs(a-b) ** num1) % 255),minVal)
        hex2 = str(hex(num2)).lstrip("0x")
        num3 = max(((num1 * num2) % 255),minVal)
        hex3 = str(hex(num3)).lstrip("0x")
        
        return ("#%s%s%s" % (hex1,hex2,hex3)).upper()
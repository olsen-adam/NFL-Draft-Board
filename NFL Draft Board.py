from res.nflAPI import refreshAPI
import res.settings as settingsModule
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updateAPI()
        
        self.settings = settingsModule
        # Set the appearance mode based on settings
        ctk.set_appearance_mode(self.settings.loadSetting("theme"))
        
        
        self.isFullScreen = self.settings.loadSetting("isFullscreen")
        self.attributes("-fullscreen", self.isFullScreen)
        
        self.title("NFL Draft Board")
        self.bind("<F11>", self.toggleFullScreen)

    def updateAPI(self):
        refreshAPI()
        
    def toggleFullScreen(self, *args):
        self.isFullScreen = not self.isFullScreen
        self.settings.setSetting("isFullscreen", self.isFullScreen)
        self.attributes("-fullscreen", self.isFullScreen)

def main():
    app = App()
    app.mainloop()
    
if __name__ == "__main__":
    main()
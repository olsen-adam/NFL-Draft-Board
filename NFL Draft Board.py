from res.NflAPI import refreshAPI
import res.Settings as settingsModule
import customtkinter as ctk
from customtkinter import CTkFont as ctkFont

class MainMenu(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settingsModule
        
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        
        self.createMainMenuButtons()
        
    def createMainMenuButtons(self):
        uiScaling = round(self.settings.loadSetting("uiScaling"))
        exitFont = ctkFont(family="Helvetica", size=35 * uiScaling, weight="bold")
        exitPadY = self.screenHeight // 10
        
        self.exitButton = ctk.CTkButton(self, text="Exit (Hold Esc)", command=self.exit, font=exitFont)
        self.exitButton.pack(side="bottom",pady=exitPadY)
        
    def exit(self): 
        self.settings.setSetting("lastWidth", self.winfo_width())
        self.settings.setSetting("lastHeight", self.winfo_height())
        self.settings.setSetting("lastX", max(0,self.winfo_x()))
        self.settings.setSetting("lastY", max(0,self.winfo_y()))
        self.destroy()

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updateAPI()
        self.settings = settingsModule
        # Set the appearance mode based on settings
        ctk.set_appearance_mode(self.settings.loadSetting("theme"))
        
        self.isFullScreen = self.settings.loadSetting("isFullscreen")
        self.attributes("-fullscreen", self.isFullScreen)
        
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        self.geometry(f"{self.settings.loadSetting("lastWidth")}x{self.settings.loadSetting("lastHeight")}+{self.settings.loadSetting('lastX')}+{self.settings.loadSetting('lastY')}")
        
        self.title("NFL Draft Board")
        self.bind("<F11>", self.toggleFullScreen)
        
        self.exitJob = None
        self.bind("<KeyPress-Escape>", self.onClosePress)
        self.bind("<KeyRelease-Escape>", self.onCloseRelease)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        
        self.mainMenu = MainMenu(self, corner_radius=10)
        self.mainMenu.pack(expand=True, fill="both", padx=10, pady=self.screenHeight // 4)

    def exit(self): 
        self.settings.setSetting("lastWidth", self.winfo_width())
        self.settings.setSetting("lastHeight", self.winfo_height())
        self.settings.setSetting("lastX", max(0,self.winfo_x()))
        self.settings.setSetting("lastY", max(0,self.winfo_y()))
        self.destroy()
    def onClosePress(self, *args): self.exitJob = self.after(1500, self.exit)
    def onCloseRelease(self, *args):
        if self.exitJob is not None:
            self.after_cancel(self.exitJob)
            self.exitJob = None
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
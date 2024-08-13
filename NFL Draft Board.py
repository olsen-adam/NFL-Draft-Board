import PIL.Image
from res.NflAPI import refreshAPI
import res.Settings as settingsModule
import customtkinter as ctk
from customtkinter import CTkFont as ctkFont
import res.Player, os, PIL

class MainMenu(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settingsModule
        
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        
        self.createMainMenuButtons()
        
    def createMainMenuButtons(self):
        self.currDir = os.path.dirname(os.path.abspath(__file__))
        self.parentDir = os.path.abspath(os.path.join(self.currDir, os.pardir))
        
        uiScaling = self.settings.loadSetting("uiScaling")
        fontSize = round(35 * uiScaling)
        buttonFont = ctkFont(family="Helvetica", size=fontSize, weight="bold")
        padY = round(75*uiScaling)
        padX = round(650*uiScaling)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.startButton = ctk.CTkButton(self, text="Start", font=buttonFont, fg_color="green", hover_color="darkgreen", height=fontSize+20)
        self.startButton.grid(row=0,column=0, padx=padX, pady=padY, sticky="ew")
        
        teamsIcon, teamsIconSize = PIL.Image.open(self.currDir + "/data/img/teams.png"), round(35 * uiScaling)
        self.teamsIcon = ctk.CTkImage(teamsIcon, size=(teamsIconSize, teamsIconSize))
        self.teamsButton = ctk.CTkButton(self,image=self.teamsIcon, text="Team Setup", font=buttonFont, height=fontSize+20)
        self.teamsButton.grid(row=1,column=0, padx=padX, pady=padY, sticky="ew")
        
        settingsIcon, settingsIconSize = PIL.Image.open(self.currDir + "/data/img/settings.png"), round(35 * uiScaling)
        self.settingsIcon = ctk.CTkImage(settingsIcon, size=(settingsIconSize, settingsIconSize))
        self.settingsButton = ctk.CTkButton(self,image=self.settingsIcon, text="Settings", font=buttonFont, height=fontSize+20)
        self.settingsButton.grid(row=2,column=0, padx=padX, pady=padY, sticky="ew")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updateAPI()
        self.settings = settingsModule
        # Set the appearance mode based on settings
        ctk.set_appearance_mode(self.settings.loadSetting("theme"))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.isFullScreen = self.settings.loadSetting("isFullscreen")
        self.attributes("-fullscreen", self.isFullScreen)
        
        self.currDir = os.path.dirname(os.path.abspath(__file__))
        self.parentDir = os.path.abspath(os.path.join(self.currDir, os.pardir))
        
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        self.scaling = self.settings.loadSetting("uiScaling")
        self.geometry(f"{self.settings.loadSetting("lastWidth")}x{self.settings.loadSetting("lastHeight")}+{self.settings.loadSetting('lastX')}+{self.settings.loadSetting('lastY')}")
        
        self.title("NFL Draft Board")
        self.bind("<F11>", self.toggleFullScreen)
        
        self.exitJob = None
        self.bind("<KeyPress-Escape>", self.onClosePress)
        self.bind("<KeyRelease-Escape>", self.onCloseRelease)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        
        self.mainMenu = MainMenu(self, corner_radius=10)
        self.mainMenu.grid(row=0,column=0,columnspan=2, sticky="nsew",padx=5,pady=5)
        
        exitIcon = PIL.Image.open(self.currDir + "/data/img/exit.png")
        buttonSize = 50
        tkImage = ctk.CTkImage(exitIcon, size=(round(buttonSize * self.scaling), round(buttonSize * self.scaling)))
        self.exitButton = ctk.CTkButton(self,image=tkImage,text=None,width=buttonSize,command=self.exit, corner_radius=10, fg_color="red", hover_color="darkred")
        self.exitButton.grid(row=1,column=0,pady=10,padx=15)
        
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
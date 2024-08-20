import PIL.Image
from res.NflAPI import refreshAPI
import res.Settings as settingsModule
import customtkinter as ctk
from customtkinter import CTkFont as ctkFont
import res.Player, os, PIL

class Settings(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def raisedFrame(self):
        settings = settingsModule.loadAllSettings()
        appScaling = settings["uiScaling"]
        settingNum = 13
        for i in range(settingNum):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # Theme
        self.themeLabel = ctk.CTkLabel(self, text="DarkMode", font=ctkFont(size=round(25 * appScaling),weight="bold"))
        self.themeSwitch = ctk.CTkSwitch(self, text="", width=round(appScaling ** 2 * 50), height=round(appScaling ** 2 * 25))
        if settings["theme"] == "dark": self.themeSwitch.toggle() 
        else: self.themeSwitch.detoggle()
        self.themeDescription = ctk.CTkLabel(self, text="Is the app in dark mode - Default: True", font=ctkFont(size=15))
        self.themeLabel.grid(row=1,column=0, sticky="e"), self.themeSwitch.grid(row=1,column=1), self.themeDescription.grid(row=1,column=2, sticky="w")
        
        # UI Scaling
        self.uiScalingLabel = ctk.CTkLabel(self, text="UI Scaling", font=ctkFont(size=round(25 * appScaling),weight="bold"))
        uiScale = ctk.DoubleVar()
        self.uiScalingSlider = ctk.CTkSlider(self, from_=0.5, to=2, number_of_steps=150, orientation="horizontal", variable=uiScale, width=round(appScaling ** 2 * 300))
        self.uiScalingSlider.set(settings["uiScaling"])
        self.uiScalingValue = ctk.CTkEntry(self, textvariable=uiScale, width=appScaling ** 2 * 50) 
        self.uiScalingLabel.grid(row=2,column=0, sticky="e"), self.uiScalingSlider.grid(row=2,column=1), self.uiScalingValue.grid(row=2,column=2,sticky="w")

class MainMenu(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settingsModule
        
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        self.teamsFinal = False
        self.isTeamsCreated()

        self.createMainMenuButtons()

    def raisedFrame(self):
        pass

    def isTeamsCreated(self,finalTeams=None):
        if finalTeams != None: self.teamsFinal = finalTeams
        if not self.teamsFinal:
            self.startButtonColour = "gray"
            self.startButtonClickable = "Disabled"
        else:
            self.startButtonColour = "green"
            self.startButtonClickable = "normal"

    def setTeamsCreated(self):
        self.isTeamsCreated(finalTeams=True)
        self.startButton.configure(fg_color=self.startButtonColour,state=self.startButtonClickable)

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
        
        self.startButton = ctk.CTkButton(self, text="Start Draft", font=buttonFont, fg_color=self.startButtonColour, hover_color="darkgreen", height=fontSize+20, state="disabled")
        self.startButton.grid(row=0,column=0, padx=padX, pady=padY, sticky="ew")
        
        teamsIcon, teamsIconSize = PIL.Image.open(self.currDir + "/data/img/teams.png"), round(35 * uiScaling)
        self.teamsIcon = ctk.CTkImage(teamsIcon, size=(teamsIconSize, teamsIconSize))
        self.teamsButton = ctk.CTkButton(self,image=self.teamsIcon, text="Team Setup", font=buttonFont, height=fontSize+20,command=self.setTeamsCreated)
        self.teamsButton.grid(row=1,column=0, padx=padX, pady=padY, sticky="ew")
        
        settingsIcon, settingsIconSize = PIL.Image.open(self.currDir + "/data/img/settings.png"), round(35 * uiScaling)
        self.settingsIcon = ctk.CTkImage(settingsIcon, size=(settingsIconSize, settingsIconSize))
        self.settingsButton = ctk.CTkButton(self,image=self.settingsIcon, text="Settings", font=buttonFont, height=fontSize+20, command=lambda: self.master.showFrame(Settings))
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
        
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        
        self.frames = {}
        
        for F in (MainMenu,Settings):
            frame = F(master=self, corner_radius=10)
            self.frames[F] = frame
            frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
                
        exitIcon = PIL.Image.open(self.currDir + "/data/img/exit.png")
        buttonSize = 50
        tkImage = ctk.CTkImage(exitIcon, size=(round(buttonSize * self.scaling), round(buttonSize * self.scaling)))
        self.exitButton = ctk.CTkButton(self,image=tkImage,text=None,width=buttonSize,command=self.exit, corner_radius=10, fg_color="red", hover_color="darkred")
        self.exitButton.grid(row=1,column=0,pady=10,padx=15)
        
        self.showFrame(MainMenu)
    
    def showFrame(self, frameClass):
        frame = self.frames[frameClass]
        frame.tkraise()
        frame.raisedFrame()
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
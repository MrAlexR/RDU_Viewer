#************************************************************#
#*  Copyright @ MrAlexR & AlbertV7 from GitHub repo 2021     *
#*  All rights reserved                                      *
#*                                                           *
#************************************************************#
import resThread as rt
import mainWindow as mw

def main():
    #Initializare thread de resurse
    rt.resThread.initialize()
    #Initializare fereastra principala
    window = mw.mainWindow()
    window.window.mainloop()

if __name__ == "__main__":
    main()
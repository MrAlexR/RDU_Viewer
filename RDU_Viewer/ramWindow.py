#************************************************************#
#*  Copyright @ MrAlexR & AlbertV7 from GitHub repo 2021     *
#*  All rights reserved                                      *
#*                                                           *
#************************************************************#
import tkinter as t
import dataCard as dc
import time
import threading
import resThread as rt
#Modul de realizare al transportului de resurse si al managementului de date
#este identic ca la celelalte ferestre. La fel si pentru administrarea thread-ului
#de date
class ramWindow:
    stopThread = False
    active = True

    def __init__(self, parent):
        self.parent = parent
        self.window = t.Tk()
        self.window.resizable(0, 0)
        self.window.title("RDU_Viewer-RAM")
        self.window.geometry('{x}x{y}'.format(x = 800, y = 500))
        self.window.configure(background = "#181818")

        self.info = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 15",
            fg = "Orange",
            text = "RAM info"
        )
        self.info.place(x = 350, y = 50)

        self.info0 = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 12",
            fg = "green",
            text = "Total: "
        )
        self.info0.place(x = 350, y = 150)

        self.info1 = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 12",
            fg = "green",
            text = "Available: "
        )
        self.info1.place(x = 350, y = 200)

        self.info2 = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 12",
            fg = "green",
            text = "Used: "
        )
        self.info2.place(x = 350, y = 250)

        self.info3 = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 12",
            fg = "green",
            text = "Free: "
        )
        self.info3.place(x = 350, y = 300)

        self.card1 = dc.dataCard(self, None ,"Usage", 150, 150, 150,
        250, "#212121", "green", 15, False)

        self.window.protocol("WM_DELETE_WINDOW", 
        lambda arg = "": self.closeWindow(arg))
        self.window.bind("<<thread_stop>>", self.closeWindow)
        self.thread1 = None
        self.startT()

    def startT(self):
        self.thread1 = threading.Thread(target = self.windowThread)
        self.thread1.start()
        self.paused = False

    def windowThread(self):
        while True:
            if self.stopThread == True or self.parent.stopThread == True:
                break
            data = rt.resThread.ram_usage
            
            try:
                self.card1.dataUsage.updateStatus(int(data[2]))
                self.info0.configure(text = "Total : {x}".format(x = data[0]))
                self.info1.configure(text = "Available : {x}".format(x = data[1]))
                self.info2.configure(text = "Used : {x}".format(x = data[3]))
                self.info3.configure(text = "Free : {x}".format(x = data[4]))
            except:
                print("memR")
            time.sleep(0.2)

        self.active = False
        self.window.event_generate("<<thread_stop>>", when = "tail")

    def closeWindow(self, event):
        self.stopThread = True
        if self.active == False:
            self.thread1.join()
            self.window.destroy()

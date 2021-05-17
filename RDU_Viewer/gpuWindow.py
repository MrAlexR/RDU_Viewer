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

class gpuWindow:
    stopThread = False
    active = True

    def __init__(self, parent):
        self.parent = parent
        self.window = t.Tk()
        self.window.resizable(0, 0)
        self.window.title("RDU_Viewer-Gpu")
        self.window.geometry('{x}x{y}'.format(x = 800, y = 500))
        self.window.configure(background = "#181818")
        self.window.protocol("WM_DELETE_WINDOW", 
        lambda arg = "": self.closeWindow(arg))
        self.window.bind("<<thread_stop>>", self.closeWindow)

        self.titleLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 20",
            fg = "Orange",
            text = "GPU Info"
        )

        self.limitLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 13",
            fg = "Orange",
            text = "Max allowed core temp {x}, limiter - {y}".format(
            x = rt.resThread.max_gput_allowed,
            y = "Off" if not rt.resThread.tempLimiter_GPU else "On")
        )
        self.limitLabel.place(x = 450, y = 380)

        self.limit = t.Button(
            master = self.window,
            bg = "orange" if rt.resThread.tempLimiter_GPU == False else "green",
            text = "Off" if rt.resThread.tempLimiter_GPU == False else "On",
            height = 2,
            width = 4,
            command = lambda: self.limiter(True if rt.resThread.tempLimiter_GPU == False else False)
        )
        self.limit.place(x = 530, y = 420)

        self.set = t.Button(
            master = self.window,
            bg = "orange",
            text = "Set",
            height = 2,
            width = 4,
            command = lambda: self.setT()
        )
        self.set.place(x = 650, y = 420)

        self.card1 = dc.dataCard(self, None ,"Usage", 150, 150, 150,
        250, "#212121", "yellow", 15, False)

        self.titleLabel.place(x = 350, y = 25)

        self.maxTemperature = t.Text(
            master = self.window,
            bg = "#181818",
            fg = "red",
            height = 1,
            width = 5,
            font = "Arial 15"
        )
        self.maxTemperature.place(x = 580, y = 420)

        self.temperatureLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 13",
            fg = "red",
            text = "GPU core temperature {x} C".format(
            x = rt.resThread.gpu_temp)
        )
        self.temperatureLabel.place(x = 450, y = 320)

        self.specs = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 15",
            fg = "Orange",
            text = "GPU specifications"
        )
        self.specs.place(x = 450, y = 150)

        self.startT()

    def startT(self):
        self.paused = False
        self.thread1 = threading.Thread(target = self.windowThread)
        self.thread1.start()

    def windowThread(self):
        while True:
            if self.stopThread == True:
                break
            if self.parent.stopThread == True:
                break
            try:
                self.temperatureLabel.configure(
                    text = "GPU core temperature {x} C".format(
                    x = rt.resThread.gpu_temp))
            except:
                print("get gput")
            try:
                self.card1.dataUsage.updateStatus(rt.resThread.gpu_freq)
            except:
                print("get gpuU")
            time.sleep(0.3)

        #Validarea inchiderii ferestrei
        self.active = False
        self.window.event_generate("<<thread_stop>>", when = "tail")  

    #Callback pentru inchiderea ferestrei
    def closeWindow(self, event):
        self.stopThread = True
        if self.active == False:
            self.thread1.join()
            self.window.destroy()

    #Callback pentru activarea sau dezactivarea restrictiei de temperatura
    def limiter(self, value):
        rt.resThread.tempLimiter_GPU = value
        self.limit.configure(text = "On" if value == True else "Off", 
        bg = "green" if value == True else "orange")
        self.limitLabel.configure(text = "Max allowed core temp {x}, limiter - {y}".format(
            x = rt.resThread.max_gput_allowed,
            y = "Off" if not rt.resThread.tempLimiter_GPU else "On"))

    #Setare temperatura maxima pentru procesor
    def setT(self):
        if rt.resThread.tempLimiter_GPU == True:
            test = self.maxTemperature.get("1.0", "end-1c")
            try:
                test = int(float(test))
            except:
                return
            rt.resThread.max_gput_allowed = test
            self.limitLabel.configure(text = "Max allowed core temp {x}, limiter - {y}".format(
            x = rt.resThread.max_gput_allowed,
            y = "Off" if not rt.resThread.tempLimiter_GPU else "On"))
    
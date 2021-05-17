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

class cpuWindow:
    #Valori initiale
    stopThread = False
    active = True
    sizeX = 800
    sizeY = 500
    
    #Initializare fereastra de cpu
    def __init__(self, parent):
        self.parent = parent
        self.window = t.Tk()
        self.window.resizable(0, 0)
        self.window.title("RDU_Viewer-Cpu")
        self.window.geometry('{x}x{y}'.format(x = 800, y = 500))
        self.window.configure(background = "#181818")
        self.window.protocol("WM_DELETE_WINDOW", 
        lambda arg = "": self.closeWindow(arg))
        self.window.bind("<<thread_stop>>", self.closeWindow)
        
        #Widget-uri de baza
        self.titleLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 20",
            fg = "Orange",
            text = "CPU Info"
        )
        self.titleLabel.place(x = 350, y = 25)
        
        self.infoLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 20",
            fg = "Orange",
            text = "General info"
        )
        self.infoLabel.place(x = 50, y = 300)

        #Preluarea datelor de baza ale PC-ului
        processor = rt.resThread.machine_stats[0]
        architecture = rt.resThread.machine_stats[1]
        machine = rt.resThread.machine_stats[2]

        #Widget-uri de baza
        self.iLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 10",
            fg = "cyan",
            text = str(processor) + "\n" +  str(architecture) + "\n" + str(machine)
        )
        self.iLabel.place(x = 50, y = 330)
        #Calcul numar segmente pentru impartirea ferestrei
        self.cpuCount = rt.resThread.cpu_core_count
        segmentSize = self.sizeX / self.cpuCount
        segmentAllocation = 80 * segmentSize / 100
        segmentMargin = 10 * segmentSize / 100
        pos = segmentMargin

        self.indicators = []
        self.coreTemps = []

        #Adauga segmentele in functie de numarul lor
        for i in range(0, self.cpuCount):
            self.indicators.append(dc.dataCard(self, None, "Core {x}".format(x = i),
            pos, 70, segmentAllocation, 200, "#212121", "yellow", 15, False))
            pos += (segmentAllocation + 2 * segmentMargin)

        for i in range(0, self.cpuCount):
            self.coreTemps.append(
                t.Label(
                    master = self.window,
                    bg = "#181818",
                    font = "Arial 10",
                    fg = "red",
                    text = "{x} C".format(x = 0)
                )
            )

        #Restul widget-urilor
        position = 450
        for i in range(0, self.cpuCount):
            self.coreTemps[i].place(x = position, y = 350)
            position += 50

        self.limit = t.Button(
            master = self.window,
            bg = "orange" if rt.resThread.tempLimiter_CPU == False else "green",
            text = "Off" if rt.resThread.tempLimiter_CPU == False else "On",
            height = 2,
            width = 4,
            command = lambda: self.limiter(True if rt.resThread.tempLimiter_CPU == False else False)
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

        self.tempLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 15",
            fg = "Orange",
            text = "Core temp Celsius"
        )
        self.tempLabel.place(x = 500, y = 300)

        self.limitLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 13",
            fg = "Orange",
            text = "Max allowed core temp {x}, limiter - {y}".format(
            x = rt.resThread.max_cput_allowed,
            y = "Off" if not rt.resThread.tempLimiter_CPU else "On")
        )
        self.limitLabel.place(x = 450, y = 380)

        self.maxTemperature = t.Text(
            master = self.window,
            bg = "#181818",
            fg = "red",
            height = 1,
            width = 5,
            font = "Arial 15"
        )
        self.maxTemperature.place(x = 580, y = 420)

        self.startT()

    #start therad 
    def startT(self):
        self.paused = False
        self.thread1 = threading.Thread(target = self.windowThread)
        self.thread1.start()

    #Thread-ul pentru modificarea valorilor din fereastra in timp real
    def windowThread(self):
        while True:
            if self.stopThread == True:
                break
            if self.parent.stopThread == True:
                break
            #utilizare si temperaturi
            
            utils = rt.resThread.cpu_core_freq
            temps = rt.resThread.cpu_temps
            
            if self.stopThread == True:
                break
            #Actualizam valorile din fereastra
            try:
                if len(temps) > 1:
                    for i in range(0, rt.resThread.cpu_core_count):
                        self.coreTemps[i].configure(text = "{x} C".format(x = temps[i]))
            except: 
                print("dispT")
            try:
                if len(utils) > 1:
                    for i in range(0, rt.resThread.cpu_core_count):
                        self.indicators[i].dataUsage.updateStatus(int(utils[i]))  
            except:
                print("distU")
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
        rt.resThread.tempLimiter_CPU = value
        self.limit.configure(text = "On" if value == True else "Off", 
        bg = "green" if value == True else "orange")
        self.limitLabel.configure(text = "Max allowed core temp {x}, limiter - {y}".format(
            x = rt.resThread.max_cput_allowed,
            y = "Off" if not rt.resThread.tempLimiter_CPU else "On"))

    #Setare temperatura maxima pentru procesor
    def setT(self):
        if rt.resThread.tempLimiter_CPU == True:
            test = self.maxTemperature.get("1.0", "end-1c")
            try:
                test = int(float(test))
            except:
                return
            rt.resThread.max_cput_allowed = test
            self.limitLabel.configure(text = "Max allowed core temp {x}, limiter - {y}".format(
            x = rt.resThread.max_cput_allowed,
            y = "Off" if not rt.resThread.tempLimiter_CPU else "On"))
    
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
import diskWindow as dw
import ramWindow as rw
import cpuWindow as cp
import gpuWindow as gw

class mainWindow():
    #Variabile necesare
    stopThread = False
    active = True
    autoSample = True
    stepIt = False
    memThread = []
    status = [False, False, False, False]
    
    def __init__(self):
        #Initializare fereastra
        self.window = t.Tk()
        self.window.resizable(0, 0)
        self.window.title("RDU_Viewer")
        self.window.geometry('{x}x{y}'.format(x = 800, y = 500))
        self.window.configure(background = "#181818")
        photo = t.PhotoImage(file = r"Resources\RDU2.png")
        self.window.iconphoto(False, photo)
        #Mesaje customizare de inchidere a ferestrei
        self.window.protocol("WM_DELETE_WINDOW", 
        lambda arg = "": self.closeWindow(arg))
        self.window.bind("<<thread_stop>>", self.closeWindow)

        #Thread-uri pentru toate sub-ferestrele
        #Flag-urile sunt pentru a determina exact ceea ce trebuie sa obtinem
        #de la thread-ul de date (pentru optimizare)
        rt.resThread.flags = [False, True, True, True, True, True, True]
        self.memThread.append(threading.Thread(target = self.memoryWindow))
        self.memThread.append(threading.Thread(target = self.diskWindow))
        self.memThread.append(threading.Thread(target = self.cpuWindow))
        self.memThread.append(threading.Thread(target = self.gpuWindow))

        #Adaugam elementele de baza ale UI-ului
        self.card1 = dc.dataCard(self, 
        lambda: self.memThread[2].start() if not self.memThread[2].is_alive() else None, "CPU", 60, 100, 150,
        250, "#212121", "green", 15, True)

        self.card2 = dc.dataCard(self, 
        lambda: self.memThread[0].start() if not self.memThread[0].is_alive() else None, "RAM", 240, 100, 150,
        250, "#212121", "yellow", 15, True)

        self.card3 = dc.dataCard(self,
        lambda: self.memThread[1].start() if not self.memThread[1].is_alive() else None, "DISK", 420, 100, 150,
        250, "#212121", "orange", 15, True)

        self.card4 = dc.dataCard(self,
        lambda: self.memThread[3].start() if not self.memThread[3].is_alive() else None, "GPU", 600, 100, 150,
        250, "#212121", "red", 15, True)

        self.aSample = t.Button(
            master = self.window,
            bg = "green",
            text = "Auto",
            height = 2,
            width = 5,
            command = lambda : self.selectMode(0)
        )
        self.aSample.place(x = 220, y = 400)

        self.manualSample = t.Button(
            master = self.window,
            bg = "cyan",
            text = "Man",
            height = 2,
            width = 5,
            command = lambda : self.selectMode(1)
        )
        self.manualSample.place(x = 270, y = 400)

        self.doSample = t.Button(
            master = self.window,
            bg = "cyan",
            text = "Smp",
            height = 2,
            width = 5,
            command = self.step
        )
        self.doSample.place(x = 320, y = 400)

        self.plusSample = t.Button(
            master = self.window,
            bg = "green",
            text = "+",
            height = 1,
            width = 1,
            command = lambda: self.sampleMod("+")
        )
        self.plusSample.place(x = 630, y = 390)

        self.minusSample = t.Button(
            master = self.window,
            bg = "red",
            text = "-",
            height = 1,
            width = 1,
            command = lambda: self.sampleMod("-")
        )
        self.minusSample.place(x = 630, y = 420)

        self.sample1Label = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 15",
            fg = "Orange",
            text = "Sample mode"
        )
        self.sample1Label.place(x = 80, y = 400)

        self.sample2Label = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 15",
            fg = "Orange",
            text = "Sample every {x} seconds".format(x = rt.resThread.sample_speed)
        )
        self.sample2Label.place(x = 380, y = 400)

        self.titleLabel = t.Label(
            master = self.window,
            bg = "#181818",
            font = "Arial 20",
            fg = "Orange",
            text = "General values"
        )
        self.titleLabel.place(x = 300, y = 25)

        #Pornim thread-ul ferestrei principale
        self.startT()
    
    #Functia de incepere a thread-ului
    def startT(self):
        self.thread1 = threading.Thread(target = self.windowThread)
        self.thread1.start()
    
    #Thread-ul ferestrei princilare
    def windowThread(self):
        while True:
            #Verificam daca se inchide fereastra
            if self.stopThread == True:
                break
            if self.autoSample == False:
                if self.stepIt != True:
                    continue
            #Obtinem datele de la thread-ul de resurse
            self.stepIt = False
            try:
                data1 = int(rt.resThread.cpu_freq)
            except: print("get cpu")
            if self.stopThread == True:
                break

            try:
                data2 = int(rt.resThread.ram_usage[2])
            except: print("get ram")
            if self.stopThread == True:
                break

            try:
                data3 = int(rt.resThread.disk_usage[3])
            except : print("get disk")

            try:
                data4 = int(rt.resThread.gpu_freq)
            except : print("get vid")

            if self.stopThread == True:
                break
            try:
                #Validam interfata cu noile valori
                self.card1.dataUsage.updateStatus(data1)
                self.card2.dataUsage.updateStatus(data2)
                self.card3.dataUsage.updateStatus(data3)
                self.card4.dataUsage.updateStatus(data4)
            except:
                print("updateError")
            
            #Actualizam thread-urile sub-ferestrelor inchise
            if not self.memThread[0].is_alive():
                self.memThread[0] = threading.Thread(target = self.memoryWindow)
            if not self.memThread[1].is_alive():
                self.memThread[1] = threading.Thread(target = self.diskWindow)
            if not self.memThread[2].is_alive():
                self.memThread[2] = threading.Thread(target = self.cpuWindow)
            if not self.memThread[3].is_alive():
                self.memThread[3] = threading.Thread(target = self.gpuWindow)
            time.sleep(0.2)

        #Procesul de inchidere al toturor thread-urilor
        self.active = False
        while True:
            ch = 0
            for st in self.status:
                ch += st
            if ch == 0:
                break
        rt.resThread.STOP_THREAD = True
        rt.resThread.THREAD1.join()
        self.window.event_generate("<<thread_stop>>", when = "tail")

    #Metoda de inchidere a ferestrei
    def closeWindow(self, event):
        self.stopThread = True
        if self.active == False:
            self.thread1.join()
            self.window.destroy()

    #Selectarea modului de esantionare al datelor manual sau automat
    def selectMode(self, mode):
        if mode is 0 :
            self.autoSample = True
            self.aSample.configure(bg = "green")
            self.manualSample.configure(bg = "cyan")
            self.doSample.configure(bg = "cyan")
        else:
            self.autoSample = False
            self.aSample.configure(bg = "cyan")
            self.manualSample.configure(bg = "green")   
            self.doSample.configure(bg = "green")
    
    #Esantionare manuala
    def step(self):
        self.stepIt = True

    #Durata timpului de esantionare - pentru cel automat
    def sampleMod(self, value):
        if value == "+":
            rt.resThread.sample_speed += 0.3
            self.sample2Label.configure(text = "Sample every {:.1f} seconds".format(
                rt.resThread.sample_speed))
        else:
            if rt.resThread.sample_speed > 0.1:
                rt.resThread.sample_speed -= 0.3
                self.sample2Label.configure(text = "Sample every {:.1f} seconds".format(
                    rt.resThread.sample_speed))
    
    #Functia de thread a ferestrei cu date ale RAM-ului
    def memoryWindow(self):
        self.status[0] = True
        wnd1 = rw.ramWindow(self)
        wnd1.window.mainloop()
        self.status[0] = False

    #Functia de thread a ferestrei cu date ale DISK-ului
    def diskWindow(self):
        self.status[1] = True
        wnd2 = dw.diskWindow(self)
        wnd2.window.mainloop()
        self.status[1] = False

    #Functia de thread a ferestrei cu date ale CPU-ului
    def cpuWindow(self):
        self.status[2] = True
        rt.resThread.flags[0] = True
        wnd3 = cp.cpuWindow(self)
        wnd3.window.mainloop()
        self.status[2] = False
        rt.resThread.flags[0] = False

    #Functia de thread a ferestrei cu date ale GPU-ului
    def gpuWindow(self):
        self.status[3] = True
        wnd4 = gw.gpuWindow(self)
        wnd4.window.mainloop()
        self.status[3] = False
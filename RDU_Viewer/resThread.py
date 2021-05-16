#************************************************************#
#*  Copyright @ MrAlexR & AlbertV7 from GitHub repo 2021     *
#*  All rights reserved                                      *
#*                                                           *
#************************************************************#
import pythoncom
import os
import time
import psutil
import platform
import threading
import wmi
import statistics as st
from datetime import datetime
import winsound as wnd

class resThread(object):
    # cpu_freq/c, cpu_freq, cpu_temp
    # ram, disk,
    # gpu, gpu_temp
    flags = [False, False, False,
            False, False,
            False, False]

    #Date PC
    machine_stats = [None, None, None]
    max_cput_allowed = 100
    max_gput_allowed = 100
    #Variabile CPU
    cpu_freq = 0
    cpu_core_count = 0
    cpu_core_freq = []
    cpu_temps = []

    gpu_freq = 0
    disk_usage = 0
    disk_part = []
    ram_usage = []

    _sensors = None

    sample_speed = 0.1
    STOP_THREAD = False
    RUNNING_THREAD = False

    tempLimiter_CPU = False
    tempLimiter_GPU = False

    THREAD1 = None
    #Functia de initializare a thread-ului de date---------------------------------------------
    @staticmethod
    def initialize():
        resThread.THREAD1 = threading.Thread(target = resThread.resourceScrapper)
        #Pornire OHM
        try:
            file1 = open(r'Resources\OHM_Config.txt', 'r')
            path = file1.readlines()
            #Data OHM nu este deschis de host, atunci il deshidem noi
            if "OpenHardwareMonitor.exe" not in (proc.name() for proc in psutil.process_iter()):
               os.startfile(path[0])
            file1.close()
            time.sleep(1)
        except:
            print("init")
        
        #Detectam datele de identificare ale PC-ului
        resThread.machine_stats[0] = platform.processor()
        resThread.machine_stats[1] = platform.architecture()
        resThread.machine_stats[2] = platform.machine()

        #detectam partitile de pe HDD/SSD  si memoria 
        resThread.disk_part = psutil.disk_partitions()
        resThread.disk_usage = psutil.disk_usage('/')

        #incarcat val initiale pt ram
        resThread.ram_usage = psutil.virtual_memory()

        #Pornim thread-ul de date
        resThread.cpu_core_count = psutil.cpu_count(logical = False)
        resThread.THREAD1.start()
        resThread.RUNNING_THREAD = True

    #Preluarea alertelor de depasire a temperaturii--------------------------------------------
    @staticmethod
    def tempWarning():
        wnd.Beep(2500, 200)
        try:
            #Inregistram alerta de temperatura si atentionam acustic
            now = datetime.now()
            data = now.strftime("%d/%m/%Y %H:%M:%S")
            print("exceded")
            file1 = open(r'Resources\TempWarning.txt', 'a')
            file1.write(str(data) + " : " + str(int(st.mean(resThread.cpu_temps))) + '\n')
            file1.close()
        except:
            print("failTW")

    #Thread-ul de date----------------------------------------------------------------------
    @staticmethod
    def resourceScrapper():
        try:
            #COM init for python
            pythoncom.CoInitialize()
            resThread._sensors = wmi.WMI(namespace="root\OpenHardwareMonitor")
        except: print("pythoncom")
        #Processing part
        while resThread.STOP_THREAD != True:
            #get cpu freq/cores
            try:
                if resThread.flags[0] == True:
                    resThread.cpu_core_freq = psutil.cpu_percent(interval=1, percpu=True)
                    if resThread.STOP_THREAD == True: break
            except:
                print("cpuC")

            #get cpu freq/cpu
            try:
                if resThread.flags[1] == True:
                    resThread.cpu_freq = int(psutil.cpu_percent(interval = 1))
                    if resThread.STOP_THREAD == True: break
            except:
                print("cpu")

            #get cpu temps/cores
            try:
                if resThread.flags[2] == True:
                    values = []
                    for sensor in resThread._sensors.Sensor():
                        if sensor.SensorType == 'Temperature':
                            if 'CPU Core' in sensor.Name:
                                values.append(float(sensor.Value))
                    resThread.cpu_temps = values
                    #Verificare temperatura admisa
                    if resThread.tempLimiter_CPU == True:
                        if st.mean(resThread.cpu_temps) > resThread.max_cput_allowed:
                            resThread.tempWarning()
                    if resThread.STOP_THREAD == True: break
            except:
                print("temp")

            #get ram usage
            try:
                if resThread.flags[3] == True:
                    resThread.ram_usage = psutil.virtual_memory()
                    if resThread.STOP_THREAD == True: break
            except:
                print("ram")

            #get disk usage
            try:
                if resThread.flags[4] == True:
                    resThread.disk_usage = psutil.disk_usage('/')
                    if resThread.STOP_THREAD == True: break
            except:
                print("ram")    

            #Delay in citirea datelor
            counter = 0
            while counter <= resThread.sample_speed:
                time.sleep(0.1)
                counter += 0.1
        
        resThread.RUNNING_THREAD = False
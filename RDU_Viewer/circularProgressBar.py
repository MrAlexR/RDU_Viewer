#************************************************************#
#*  Copyright @ MrAlexR & AlbertV7 from GitHub repo 2021     *
#*  All rights reserved                                      *
#*                                                           *
#************************************************************#
import tkinter as t

class circularProgressBar:
    def __init__(self, master, size, posX, posY, 
                bgcolor, fgcolor, thickness, start, stop, ts, dt):
        self.canvasBase = t.Canvas(
            master = master,
            bg = bgcolor,
            height = size,
            width = size,
            highlightthickness = 0
        )

        coord = 10*size/100, 10*size/100, 90*size/100, 90*size/100,
        cap2 = self.canvasBase.create_oval(coord[0],
                                        coord[1], 
                                        coord[2],
                                        coord[3], 
                                        fill = "Cyan",
                                        outline = "")
        
        self.progressBar = self.canvasBase.create_arc(
            coord,
            start = start,
            extent = stop,
            fill = fgcolor,
            style = t.PIESLICE
        )

        r = 80 * size / 200

        cap = self.canvasBase.create_oval(size / 2 - thickness * r / 100,
                                    size / 2 - thickness * r / 100, 
                                    size / 2 + thickness * r / 100,
                                    size / 2 + thickness * r / 100, 
                                    fill = bgcolor,
                                    outline = "")
        self.canvasBase.place(x = posX, y = posY)
        self.newstatus = self.canvasBase.create_text(
            size / 2,
            size / 2,
            fill = fgcolor,
            font = "Arial {x}".format(x = ts),
            text = "{x}%".format(x = stop * 100 / 360)
        )
    
    def updateStatus(self, value):
        try:
            self.canvasBase.itemconfig(self.progressBar, extent = value * 360 / 100)
            self.canvasBase.itemconfig(self.newstatus, 
            text="{x}%".format(x = int(value)))
        except:
            print("tk error")
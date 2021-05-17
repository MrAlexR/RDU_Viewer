#************************************************************#
#*  Copyright @ MrAlexR & AlbertV7 from GitHub repo 2021     *
#*  All rights reserved                                      *
#*                                                           *
#************************************************************#
import tkinter as t
import circularProgressBar as cb

class dataCard():
    def __init__(self, root, function, title, px, py, sizex, sizey, bg, fg, tsize, dt):
        self.cardCanvas = t.Canvas(
            master = root.window,
            bg = bg,
            height = sizey,
            width = sizex,
            highlightthickness = 0
        )

        self.titleLabel = self.cardCanvas.create_text(
            75,
            sizey / 6,
            fill = fg,
            font = "Arial {x}".format(x = tsize),
            text = title
        )

        self.details = t.Button(
            master = self.cardCanvas,
            bg = fg,
            text = "Detalii",
            height = 2,
            width = 5,
            command = lambda: function()
        )
        if dt == True:
            self.details.place(x = 55, y = sizey / 4)

        self.dataUsage = cb.circularProgressBar(self.cardCanvas, 50 * sizey / 100,
        (sizex - (50 * sizey / 100)) / 2, 40 * sizey / 100, bg,
        fg, 80, 90, 270, 15, dt)

        self.cardCanvas.place(x = px, y = py)
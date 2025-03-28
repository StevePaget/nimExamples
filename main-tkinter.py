import tkinter as tk
from tkinter import font as tkFont
import random
from playsound import playsound

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("950x900+0+0")
        self.theCanvas = tk.Canvas(self,width=800, height=900, bg="#ddddff")
        self.theCanvas.grid(row=0, column=0,rowspan=4)
        self.buttonfont = tkFont.Font(family="Consolas", weight="bold")
        self.mainfont = tkFont.Font(family="Consolas", size=22, weight="bold")

        self.button1 = tk.Button(self, text="Done", font=self.buttonfont, command = self.doneclicked)
        self.button1.grid(row=1, column=1,sticky="NSEW")
        self.button2 = tk.Button(self, text="Undo", font=self.buttonfont, command = self.undoclicked)
        self.button2.grid(row=2, column=1,sticky="NSEW")
        self.rowconfigure(3,weight=1)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        
        self.theCanvas.bind("<Motion>", self.mouseMoved)
        self.theCanvas.bind("<Button-1>", self.mouseClicked)

        
        self.movetext=None
        self.infotext = None
        self.stonepic = tk.PhotoImage(file="stone.png")


        self.columnchosen = None
        self.numberchosen = 0
        self.gamestate = 0 # 0 is human turn
        self.stonepics = []
        self.setupGame()
        self.mainloop()


    def doneclicked(self):
        if self.gamestate == 1:  # computer's turn, so no clicking allowed
            return
        if self.columnchosen is None or self.numberchosen == 0:
            playsound("bad.wav",block=False)
            self.theCanvas.delete(self.infotext)
            self.infotext = self.theCanvas.create_text(750,20, text=f"You must choose some stones", anchor="ne", font=self.mainfont)
            return
        self.theCanvas.delete(self.infotext)
        self.infotext = self.theCanvas.create_text(750,20, text=f"Computer Player's turn", anchor="ne", font=self.mainfont)
        playsound("good.wav", block=False)
        self.piles[self.columnchosen] -= self.numberchosen
        self.columnchosen = None
        self.numberchosen = 0
        self.drawBoard()
        self.gamestate = 1
        # now Do Computer Turn!


    def undoclicked(self):
        if self.gamestate == 1:  # computer's turn, so no clicking allowed
            return
        playsound("click.wav", block=False)
        self.theCanvas.itemconfig(self.infotext,text="Undo clicked")
        self.columnchosen = None
        self.numberchosen = 0
        self.drawBoard()

    def mouseMoved(self,e):
        self.theCanvas.delete(self.movetext)
        self.movetext = self.theCanvas.create_text(20,20, text=f"moved to {e.x}, {e.y}", anchor="nw")

    def mouseClicked(self,e):
        if self.gamestate == 1:  # computer's turn, so no clicking allowed
            return
        column = e.x//200
        self.theCanvas.delete(self.infotext)
        self.infotext = self.theCanvas.create_text(750,20, text=f"Chose Column {column}", anchor="ne", font=self.mainfont)
        if self.columnchosen is None:
            self.columnchosen = column
        if self.columnchosen != column:
            self.theCanvas.itemconfig(self.infotext,text="You can only choose one pile", font=self.mainfont)
            playsound("bad.wav", block=False)
        else:
            self.theCanvas.itemconfig(self.infotext,text="OK", font=self.mainfont)
            self.numberchosen +=1
            playsound("lay2.wav", block=False)
            if self.piles[self.columnchosen]<self.numberchosen:
                self.numberchosen = self.piles[self.columnchosen]
            self.drawBoard()

    def setupGame(self):
        self.piles = [7,5,3,1]
        self.drawBoard()

    def drawBoard(self):
        # delete all the old stone pictures
        for s in self.stonepics:
            self.theCanvas.delete(s)
        self.stonepics = []
        # draw the piles of stones
        # Go through each value in self.piles
        # draw the right number of stones in the right place

        y = 300
        x = 100
        for pilenum in range(len(self.piles)):
            if pilenum == self.columnchosen:
                reduction = self.numberchosen
            else:
                reduction = 0
            for stoneNum in range(self.piles[pilenum] - reduction):
                self.stonepics.append(self.theCanvas.create_image(x,y,image=self.stonepic))
                y += 50
            x += 200
            y = 300

app = Main()

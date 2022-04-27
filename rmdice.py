#!/usr/bin/env python

import os
import random

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape


class RollnWriteGame:
    
    remsize = (1404,1872)
    
    def __init__(self, name, image):
        random.seed()
        self.c = canvas.Canvas(name, pagesize=landscape(self.remsize)) # bottomup=0,
        # first page
        self.c.bookmarkPage('Sheet')
        self.c.drawImage(image, 0,0, self.remsize[1], self.remsize[0])
        self.debug = False

    def link(self, topage, x, y, w=1, h=1):
        self.c.linkRect('link to '+topage, topage,
                (x, y, x+w, y+h),
                Border='[0 0 0]')

    def linkDice(self, rect , maxdice):
        """ @param dice link to 1..dice (dice included)"""
        x,y,w,h = rect
        y = self.remsize[0]-y-h
        for ix in range(x,x+w):
            for iy in range(y,y+h):
                p = random.randint(1, maxdice)
                self.link(f'Dice{p}', ix,iy)
        if self.debug:
            self.c.rect(x,y,w,h)

    def addPage(self, dice):
        self.c.showPage()
        self.c.bookmarkPage(f'Dice{dice}')
        
    def drawBackDice(self, dice, x=100, y=100, w=50, h=50):
        #x,y,w,h = rect
        y = self.remsize[0]-y-h
        self.link('Sheet', x,y,w,h)
        self.c.rect(x,y,w,h)
        self.c.setFont("Times-Roman", 50)
        self.c.drawString(x+10, y+10, str(dice))

    def save(self):
        self.c.save()

datadir = 'games/rollncook'
builddir = 'build'
pdf = builddir + '/rmRollnCook-intro.pdf'

def createSheet():
    sheet = datadir+'/RollnCook-Sheet.jpg'
    dices = 6*6*6
    rdices = (1565,215,180,60)

    xdice,ydice,wdice,hdice = rdices
    wdice = wdice/3

    game = RollnWriteGame(pdf, sheet)
    game.linkDice(rdices, dices)

    # dices pages
    for d3 in range(6):
        for d2 in range(6):
            for d1 in range(6):
                dice = 1 + d1 + d2*6 + d3*36
                game.addPage(dice)
                game.drawBackDice(d1+1, xdice,ydice,wdice,hdice)
                game.drawBackDice(d2+1, xdice+wdice,ydice,wdice,hdice)
                game.drawBackDice(d3+1, xdice+2*wdice,ydice,wdice,hdice)

    game.save()

def addRules():
    from PyPDF2 import PdfFileMerger

    merger = PdfFileMerger()

    input1 = open(datadir+'/rmRollnCook-regles.pdf', 'rb')
    input2 = open(pdf, 'rb')

    merger.append(fileobj=input1, pages=(0, 4))
    merger.append(input2)

    input1.close()
    input2.close()

    output = open(pdf, 'wb')
    merger.write(output)
    output.close()

    merger.close()


os.makedirs(builddir)
createSheet()
addRules()

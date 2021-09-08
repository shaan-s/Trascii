def drawribbon(x,title,options):
    global win, bahnschrift, bahnsmall, ropen, click
    xpos = x*100
    rect = pygame.Rect(xpos,0,100,50)
    mousepos = pygame.mouse.get_pos()
    if pygame.Rect.collidepoint(rect,mousepos) or (ropen[x] and pygame.Rect.collidepoint(pygame.Rect(xpos,0,100,50*(len(options)+1)),mousepos)):
        ropen[x] = True
    else:
        ropen[x] = False
    pygame.draw.rect(win, (40,40,40), rect, 0)
    head = bahnschrift.render(title,True,(135, 135, 235))
    win.blit(head,(xpos + (100 - head.get_rect().width) // 2 ,5))

    if ropen[x]:
        for i in range(len(options)):
            optionrect = pygame.Rect(xpos,(i+1)*50,100,50)
            if pygame.Rect.collidepoint(optionrect,mousepos):
                pygame.draw.rect(win, (80,80,80), optionrect, 0)
                if click:
                    return i
            else:
                pygame.draw.rect(win, (100,100,100), optionrect, 0)
            desc = bahnsmall.render(options[i],True,(135, 135, 235))
            win.blit(desc,(xpos + (100 - desc.get_rect().width) // 2,((i+1)*50)+10))
    return -1
def save():
    file = easygui.filesavebox(default="New Text File.txt")
    f = open(file, "w")
    if img:
        f.write(f"[{imgpath},{imgscale},{imgopacity},{imgoffset}]\n")
    else:
        f.write("[]")
    for line in text:
        for char in line:
            f.write(char)
        f.write("\n")
    f.close()

import pygame
import easygui
from time import time
from numpy import add,all
import os

import fontselect

pygame.init()

run = True
click = False
win = pygame.display.set_mode((600,600), pygame.RESIZABLE)
pygame.display.set_caption("Trascii Editor v0.5")
imgscale = 1
imgopacity = 204
imgoffset = [0,0]

img = False
typing = True
ropen = [False,False,False,False,False,False,False,False,False,False,False,False]
text = [[]]
currentline = 0
fontsize = 12
linespacingiv = 1.5
typeface = "couriernew"

typeimg = pygame.image.load("typingindicator.png")
editimg = pygame.image.load("editindicator.png")

bgcol = [(235,235,255), (235,235,235)] #Edit colour; typing colour
black = (0,0,0)
blinker = [0,0]

bahnschrift = pygame.font.SysFont("bahnschrift", 25, 0, 0)
bahnsmall = pygame.font.SysFont("bahnschrift", 15, 0, 0)

while run:
    couriernew = pygame.font.SysFont(typeface, round(fontsize*1.66666666667), 0, 0)
    linespacing = round(linespacingiv * fontsize + fontsize)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL:
                if event.key == pygame.K_EQUALS:
                    fontsize += 1
                if event.key == pygame.K_MINUS:
                    fontsize -= 1
            if event.key == pygame.K_ESCAPE:
                typing = not typing
                continue
            if not(typing):
                while len(text) < blinker[1]+1:
                    text.append([])
                while len(text[blinker[1]]) < blinker[0]+1:
                    text[blinker[1]].append(" ")
                text[blinker[1]][blinker[0]] = event.unicode
            else:
                if pygame.K_UP <= event.key <= pygame.K_LEFT:
                    hold = add(blinker,[[0,-1],[0,1],[1,0],[-1,0]][[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT].index(event.key)])
                    if hold[0] >= 0 and hold[1] >= 0:
                        blinker = hold
                elif event.key == pygame.K_BACKSPACE:
                    if blinker[0] == 0 and blinker[1] != 0:
                        text[blinker[1]-1] += text[blinker[1]]
                        text.pop(blinker[1])
                        blinker[1] -= 1
                        blinker[0] = len(text[blinker[1]])
                    elif not text[blinker[1]] and blinker[1] != 0:
                        text.pop(blinker[1])
                        blinker[1] -= 1
                        blinker[0] = len(text[blinker[1]])
                    elif text[blinker[1]] != [] and blinker[0]-1 >= 0:
                        text[blinker[1]].pop(blinker[0]-1)
                        blinker[0] -= 1

                elif event.key == pygame.K_RETURN:
                    blinker[1] += 1
                    blinker[0] = 0
                    text.insert(blinker[1],[])
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_SPACE:
                    spc = easygui.integerbox("Please enter how many spaces you want to insert","Insert Spaces",1,1,20)
                    text[blinker[1]] += " "*spc
                    blinker[0] += spc
                else:
                    text[blinker[1]].insert(blinker[0],event.unicode)
                    blinker[0] += 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            mxy = pygame.mouse.get_pos()
            if not typing:
                blinker = [(mxy[0]-5)//fontsize,(mxy[1]-50)//linespacing]
            if pygame.Rect.collidepoint(pygame.Rect(win.get_width()-90,win.get_height()-90,80,80),mxy):
                typing = not typing
        else:
            click = False
    while blinker[1] > len(text)-1:
        text.append([])
    while blinker[0] > len(text[blinker[1]]):
        text[blinker[1]].append(" ")
    win.fill(bgcol[typing])
    if img:
        trace.set_alpha(imgopacity)
        win.blit(pygame.transform.scale(trace, (round(600*imgscale),round(600*imgscale*trace.get_height()/trace.get_width()))), (0+imgoffset[0],50+imgoffset[1]))
    if not typing:
        for y in range(40):
            for x in range(200):
                if [x,y] == blinker:
                    pygame.draw.rect(win, (195, 160, 255), (5+x*fontsize,50+y*linespacing,fontsize,linespacing), 0)
                pygame.draw.rect(win, (135, 135, 235), (5+x*fontsize,50+y*linespacing,fontsize,linespacing), 1)
    else:
    #Draw Blinker:
        if int(str(round(time(),1))[-1]) > 5:
            pygame.draw.rect(win, (40,40,40), (5+blinker[0]*fontsize,50+blinker[1]*linespacing,0,linespacing), 0)

    counter = 0
    for x in text:
        win.blit(couriernew.render("".join(x),True,black),(5,50+linespacing*counter))
        counter += 1
    #fix invalid unicode characters that become ""
    for xars in range(len(text)):
        for yars in range(len(text[xars])):
            if text[xars][yars] == "":
                text[xars][yars] = " "
    #Draw Header:
    pygame.draw.rect(win, (135, 135, 235), (0,0,2000,50), 0)
    file = drawribbon(0,"File",["Save","Load"])
    if file == 0:
        save()
    elif file == 1:
        if text != [[]]:
            if easygui.boolbox("Would you like to save before loading?","Wait",["Yes","No"]):
                save()
        #try:
        loadfilename = easygui.fileopenbox()
        read = open(loadfilename).read().splitlines()
        text = []
        if loadfilename[-8:] == ".trascii":
            if read[0] != "[]":
                imgpath,imgscale,imgopacity,imgoffset = list(read[0])
                read.pop(0)
                trace = pygame.image.load(imgpath)
        for line in read:
            text.append(list(line))

    image = drawribbon(1,"Image",["Load","Scale","Opacity","Offset"])
    if image == 0:
        #Load image
        try:
            imgpath = easygui.fileopenbox()
            trace = pygame.image.load(imgpath)
            img = True
        except:
            print("Error: Image failed to upload")

    elif image == 1:
        try:
            imgscale = float(easygui.enterbox("Please enter desired image scale! (Default 1)","Image Options: Image Scale",imgscale))
        except:
            easygui.msgbox("Something went wrong! Make sure you are inputing numbers only!")
            imgscale = 1
    elif image == 2:
        try:
            imgopacity = int(easygui.enterbox("Please enter the desired image opacity, between 1 and 100! (Default 80%)","Image Options: Image Opacity",imgopacity/2.55))*2.55
        except:
            easygui.msgbox("Something went wrong! Make sure you are inputing numbers only!")
            imgopacity = 204
    elif image == 3:
        try:
            imgoffset[0] = int(easygui.enterbox("Please enter the desired image X axis offset, in pixels (Default 0)","Image Options: Image Offset",0))
            imgoffset[1] = int(easygui.enterbox("Please enter the desired image Y axis offset, in pixels (Default 0)","Image Options: Image Offset",0))
        except:
            easygui.msgbox("Something went wrong! Make sure you are inputing numbers only!")
    fontbox = drawribbon(2,"Font",["Size","Line Spacing","Typeface"])
    try:
        if fontbox == 0:
            fontsize = easygui.integerbox("Please enter the desired font size, in pixels (Default 12)","Font Options: Size")
        elif fontbox == 1:
            linespacingiv = float(easygui.enterbox("Please enter the desired line spacing, in relative font heights (Default 1.5)","Font Options: Spacing"))
    except:
        fontsize = 12
        linespacing = 1.5
    if fontbox == 2:
        typeface = fontselect.menu(sorted(pygame.font.get_fonts()))
        win = pygame.display.set_mode((600,600), pygame.RESIZABLE)
        pygame.display.set_caption("Trascii Editor v0.5")
    win.blit(pygame.transform.scale([editimg,typeimg][typing], (80,80)),(win.get_width()-90,win.get_height()-90))
    pygame.display.update()
if easygui.boolbox("Would you like to save before quitting?","Wait",["Yes","No"]):
    save()
pygame.quit()

input("Press ENTER to exit console.")

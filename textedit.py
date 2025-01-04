def drawribbon(x,title,options): #Draw top menu GUI
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

def export(): #File -> Export. Saves a txt file
    file = easygui.filesavebox(default="New Export.txt")
    if not file: return
    f = open(file, "w")
    for line in text:
        for char in line:
            f.write(char)
        f.write("\n")
    f.close()

def save(): #File -> Save. Saves a .trascii file.
    file = easygui.filesavebox(default="New Text File.trascii")
    if not file: return
    f = open(file, "w")
    if img:
        try:
            newpath = imgpath.replace("\\","\\\\")
        except:
            pass
        f.write(f"['{newpath}',{imgscale},{imgopacity},{imgoffset}]\n")
    else:
        f.write("[]")
    for line in text:
        for char in line:
            f.write(char)
        f.write("\n")
    f.close()

def arrows(): #???
    global blinker
    hold = add(blinker,[[0,-1],[0,1],[1,0],[-1,0]][[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT].index(event.key)])
    if hold[0] >= 0 and hold[1] >= 0:
        blinker = [hold[0],hold[1]]

def error_handling(e):
    print(f"{round(time())}: Error: {e}")
    e = str(e)
    if e == "Unsupported image format":
        easygui.msgbox("Image upload failed: unsupported image format. Please make sure you are uploading an image that is .png, .jpg, .gif, or .bmp. ")
    elif e == "not a file object":
        easygui.msgbox("File upload failed: please make sure you select a file. ")
    else:
        easygui.msgbox("An unknown error occured! Please see the console for details. ")

def is_char_valid():
    validchar = True
    if charset in [0,1] and not event.unicode.isprintable():
        validchar = False
    if charset in [0,2] and not event.unicode.isascii():
        validchar = False
    if event.unicode == "":
        validchar = False
    if validchar:
        return validchar

try: #Failsafe (don't lose work even if it crashes)
    import pygame
    import easygui
    from time import time
    from numpy import add
    from ast import literal_eval

    import fontselect #from fontselect.py

    pygame.init()
    win = pygame.display.set_mode((600,600), pygame.RESIZABLE)

    run = True
    click = False
    imgscale = 1
    imgopacity = 204
    imgoffset = [0,0]
    caption_text = "Trascii Editor v0.8"

    loadfilename = ""
    img = False
    typing = True
    ropen = [False,False,False,False,False,False,False,False,False,False,False,False]
    text = [[]]
    currentline = 0
    fontsize = 12
    linespacingiv = 1
    typeface = "couriernew"
    charset = 0


    pygame.display.set_caption(f"{caption_text}")
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
        if loadfilename:
            pygame.display.set_caption(f"{caption_text}: {loadfilename}")
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
                    if typeface == "couriernew":
                        typing = not typing
                    elif easygui.boolbox("Edit mode is only enabled on the font Courier New. Would you like to switch to this font?","Notice",["Yes","No"]):
                        typeface = "couriernew"
                    continue

                if not(typing): #edit mode keys only
                    while len(text) < blinker[1]+1:
                        text.append([])
                    while len(text[blinker[1]]) < blinker[0]+1:
                        text[blinker[1]].append(" ")
                    if pygame.K_RIGHT <= event.key <= pygame.K_UP:
                        arrows()
                    elif event.key == pygame.K_BACKSPACE:
                        text[blinker[1]][blinker[0]] = " "
                    elif is_char_valid():
                        text[blinker[1]][blinker[0]] = event.unicode
                        blinker[0] += 1

                else: #typing mode keys only
                    if event.key == pygame.K_BACKSPACE:
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
                    if event.key == pygame.K_RETURN:
                        blinker[1] += 1
                        blinker[0] = 0
                        text.insert(blinker[1],[])
                    elif mods & pygame.KMOD_CTRL and event.key == pygame.K_SPACE:
                        spc = easygui.integerbox("Please enter how many spaces you want to insert","Insert Spaces",1,1,20)
                        text[blinker[1]] += " "*spc
                        blinker[0] += spc
                    elif is_char_valid():
                        text[blinker[1]].insert(blinker[0],event.unicode)
                        blinker[0] += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                mxy = pygame.mouse.get_pos()
                if not typing:
                    blinker = [(mxy[0]-5)//fontsize,(mxy[1]-50)//linespacing]
                if pygame.Rect.collidepoint(pygame.Rect(win.get_width()-90,win.get_height()-90,80,80),mxy):
                    if typeface == "couriernew":
                        typing = not typing
                    elif easygui.boolbox("Edit mode is only allowed on the font Courier New. Would you like to switch to this font?","Notice",["Yes","No"]):
                        typeface = "couriernew"
            else:
                click = False
        while blinker[1] > len(text)-1:
            text.append([])
        while blinker[0] > len(text[blinker[1]]):
            text[blinker[1]].append(" ")
        win.fill(bgcol[typing])

        if img and not pygame.key.get_pressed()[pygame.K_F1]:
            trace.set_alpha(imgopacity)
            win.blit(pygame.transform.scale(trace, (round(600*imgscale),round(600*imgscale*trace.get_height()/trace.get_width()))), (0+imgoffset[0],50+imgoffset[1]))
        if not typing:
            for y in range(40):
                for x in range(200):
                    if [x,y] == blinker:
                        blinker_rect = pygame.Rect(5+x*fontsize,50+y*linespacing,fontsize,linespacing) #draw transparent rect from https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
                        shape_surf = pygame.Surface(blinker_rect.size, pygame.SRCALPHA)
                        pygame.draw.rect(shape_surf, (195, 160, 255, 100), shape_surf.get_rect())
                        win.blit(shape_surf, blinker_rect)
                    pygame.draw.rect(win, (135, 135, 235), (5+x*fontsize,50+y*linespacing,fontsize,linespacing), 1)
        else:
        #Draw Blinker:
            if int(str(round(time(),1))[-1]) > 5:
                pygame.draw.rect(win, (40,40,40), (5+blinker[0]*fontsize,50+blinker[1]*linespacing,1,fontsize*2), 0)

        counter = 0
        for x in text:
            win.blit(couriernew.render("".join(x),True,black),(5,50+linespacing*counter))
            counter += 1

        #Draw Header:
        pygame.draw.rect(win, (135, 135, 235), (0,0,2000,50), 0)
        file = drawribbon(0,"File",["Save","Open","Export","Charset"])
        if file == 0:
            save()
        elif file == 1:
            try:
                if text != [[]]:
                    if easygui.boolbox("Would you like to save before loading?","Wait",["Yes","No"]):
                        save()
                loadfilename = easygui.fileopenbox()
                read = open(loadfilename).read().splitlines()
                text = []
                prefix = loadfilename.split(".")[-1]
                if prefix not in ["trascii","txt"]:
                    prefix = ["trascii","txt"][easygui.boolbox("This file name is not a supported type (.txt or .trascii). Which would you like to treat it as?","Error",["Text file","Trascii file"])]
                if prefix == "trascii": #trascii file
                    print(literal_eval(read[0]))
                    if read[0] != "[]":
                        imgpath,imgscale,imgopacity,imgoffset = literal_eval(read[0])
                        img = True
                        read.pop(0)
                        trace = pygame.image.load(imgpath)
                for line in read:
                    text.append(list(line))
            except Exception as e:
                if loadfilename == None:
                    e = "not a file object"
                error_handling(e)
                easygui.msgbox("Make sure the file you are opening is a .txt or .trascii file (or otherwise .txt adjacent).")

        elif file == 2:
            export()
        elif file == 3:
            charsetoptions = ["1) Printable ASCII characters (reccomended)","2) Printable characters only", "3) ASCII characters only", "4) No restricitons"]
            charset = charsetoptions.index(easygui.buttonbox(f"Please pick a character set. The charset is currently set to {charset+1}","File Options: Charset",charsetoptions))
        image = drawribbon(1,"Image",["Load","Scale","Opacity","Offset"])
        if image == 0:
            #Load image
            try:
                imgpath = easygui.fileopenbox()
                trace = pygame.image.load(imgpath)
                img = True
            except Exception as e:
                error_handling(e)

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
                fontsize = int(easygui.integerbox("Please enter the desired font size, in pixels (Default 12)","Font Options: Size"))
            elif fontbox == 1:
                linespacingiv = float(easygui.enterbox("Please enter the desired line spacing, in relative font heights (Default 1.5)","Font Options: Spacing"))
        except:
            fontsize = 12
            linespacing = 1.5
        if fontbox == 2:
            typeface = fontselect.menu(sorted(pygame.font.get_fonts()))
            typing = True
            win = pygame.display.set_mode((600,600), pygame.RESIZABLE)
            pygame.display.set_caption(f"{caption_text}")
        win.blit(pygame.transform.scale([editimg,typeimg][typing], (80,80)),(win.get_width()-90,win.get_height()-90))
        pygame.display.update()

    if easygui.boolbox("Would you like to save before quitting?","Wait",["Yes","No"]):
        save()
    pygame.quit()
    input("Press ENTER to exit console.")
except Exception as e:
    easygui.msgbox("Something went wrong! (A crash has occured):" + str(e))
    save()

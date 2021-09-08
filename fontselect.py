#adapted from /Actually tryna make a game/menu.py
import pygame
from sys import exit
pygame.init()

def menu(maps):
    rects = {}
    run = True
    name = False
    scroll = 0
    win = pygame.display.set_mode((500,690))
    pygame.display.set_caption("Font Options: Typeface")

    def render(txt,pos,fnt):
        if name:
            win.blit(pygame.font.SysFont("Arial", 20).render(txt, True, (255,255,255)), pos)
        else:
            try:
                win.blit(pygame.font.SysFont(fnt, 20).render(txt, True, (255,255,255)), pos)
            except:
                win.blit(pygame.font.SysFont("Arial", 20).render(txt, True, (255,255,255)), pos)

    while run:
        win.fill((40,40,40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               exit()
            elif pygame.mouse.get_pressed()[0]:
                for item in rects:
                    if pygame.Rect.collidepoint(rects[item],pygame.mouse.get_pos()):
                        #pygame.quit()
                        return item
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll != 0:
                    scroll -=1
                elif event.button == 5:
                    scroll +=1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    name = not name

        render("Please select a typeface", (10,10), "Arial")
        win.blit(pygame.font.SysFont("Arial", 12).render("Press escape to see unchanged font names.", True, (200,200,200)), (240,20))
        ypos = 40
        for term in maps[scroll:scroll+13]:
            crect = pygame.Rect(10,ypos,480,45)
            pygame.draw.rect(win, (20,20,20), crect)
            render(term,(20,ypos+10),term)
            rects[term] = crect
            ypos += 50
        pygame.display.update()

if __name__ == "__main__":
    print(menu(sorted(pygame.font.get_fonts())))

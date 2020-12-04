import pygame as pg

pg.init()

overflate = pg.display.set_mode((500,350))

pg.display.set_caption("Spill")
bg = pg.image.load("carrot.png")
link = pg.image.load("carrot.png")
linkx = 0
linky = 0

overflate.blit(link,(linkx, linky))
pg.display.update()

overflate.blit(bg,(0, 0))
pg.display.update()

while True:
    for e in pg.event.get():
        if e.type == pg.K_w:
                spillerx+=10
        if e.type == pg.QUIT:
            pg.quit()
    pg.display.update()
from classes import Particle, Player, Block, Laser, Box, Camera, Button, Arrow
from random import uniform, randint
import pygame
import math
import time

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
death = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
death.fill((255, 0, 0))
death.set_alpha(100)
hsfont = pygame.font.SysFont("timesnewroman", 36)

died_sound = pygame.mixer.Sound("sounds/died.wav")
level_win_sound = pygame.mixer.Sound("sounds/level_win.wav")

def load(name, dim):
    return pygame.transform.scale(pygame.image.load(name), dim)


def getint(list):
    return tuple(map(int, list))


im = pygame.image.load("player.png")

screen = pygame.display.set_mode((500, 500))
DOWN = math.pi / 2


def level1():

    player = Player(im, (-1050, 250))
    level = open("level1.txt", "r")
    blocks = level.read().split("\n")
    cam = Camera(screen, player)
    endblock = Block((150, 150), (20, 20, 175), (463, 440), cam)
    Arrow(270, (-1050, 250), cam)
    Arrow(180, (585, -475), cam)
    Arrow(270, (535, 520), cam)
    rectlist = []
    for item in blocks:
        info = item.split(" ")

        topleft = getint(info[0].split(","))
        dim = getint(info[1].split(","))
        colour = getint(info[2].split(","))

        rectlist.append(Block(dim, colour, topleft, cam))
    llist = [
        Laser((98, -80), (141, -310)),
        Laser((363, 420), (363, 300)),
        Laser((86, 420), (86, 300))
    ]
    button = Button(load("upbut.png", (70, 24)), load("downbut.png", (70, 24)),
                    (290, 58), llist[0], cam)
    box = Box(load("box.png", (50, 50)), player, (167, -75), cam)
    rectlist.append(box)
    done = False
    clock = pygame.time.Clock()
    jet = False
    while not done:
        if player.rect.bottom > 750:
            player.dead = True
        clock.tick(30)
        gas = player.grounded
        pygame.event.pump()
        screen.fill((255, 255, 255))
        for item in llist:

            item.update(player)
        button.update(rectlist, player)
        box.update(rectlist, clock.get_time())
        #print(player.rect.collidelist(rectlist))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    jet = True

        player.move(pygame.key.get_pressed(), jet, clock.get_time(), rectlist)

        cam.draw()
        if gas:

            jet = False

        cam.pos = (player.pos[0] - 250, player.pos[1] - 250)
        if player.pos[1] > 600:
            #player.die()
            pass
        #print(player.vector)
        pygame.display.flip()
        if player.dead:
            pygame.mixer.Sound.play(died_sound)
            done = True
            screen.blit(death, (0, 0))
            pygame.display.flip()
            time.sleep(0.2)
            level1()
        if player.rect.colliderect(endblock.rect):
            pygame.mixer.Sound.play(level_win_sound)
            print("next level")
            time.sleep(2)

            done = True
            level2()


def level2():
    player = Player(im, (-1275, 250))

    level = open("level2.txt", "r")
    blocks = level.read().split("\n")
    cam = Camera(screen, player)
    k = Arrow(270, (-1275, 125), cam)

    endblock = Block((250, 225), (20, 20, 200), (-1853, -550), cam)
    cam.dlist.append(Arrow(90, (-1670, -400), cam))
    b = Arrow(0, (790, 385), cam)
    b.image = pygame.image.load("jetpack.png")
    Arrow(90, (760, 325), cam)
    #endblock = Block()
    rectlist = []
    for item in blocks:
        info = item.split(" ")

        topleft = getint(info[0].split(","))
        dim = getint(info[1].split(","))
        colour = getint(info[2].split(","))

        rectlist.append(Block(dim, colour, topleft, cam))
    llist = [
        Laser((-600, 375), (-830, 280)),
        Laser((170, 670), (170, 550)),
        Laser((345, 670), (345, 550))
    ]
    mid = (-600, 325)

    done = False
    clock = pygame.time.Clock()
    jet = False
    f = 0
    while not done:
        if player.rect.bottom > 700:
            player.dead = True
        if b.rect.colliderect(player.rect) and b in cam.dlist:
            cam.dlist.remove(b)
            player.hasjet = True
            k.image = pygame.transform.rotate(k.image, 45)

        f -= 0.1
        llist[0].end = (math.sin(f) * 232 + mid[0], math.cos(f) * 232 + mid[1])
        llist[0].start = (math.sin(f + math.pi) * 232 + mid[0],
                          math.cos(f + math.pi) * 232 + mid[1])

        clock.tick(30)
        gas = player.grounded
        pygame.event.pump()
        screen.fill((255, 255, 255))
        for item in llist:

            item.update(player)

        #print(player.rect.collidelist(rectlist))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    jet = True

        player.move(pygame.key.get_pressed(), jet, clock.get_time(), rectlist)

        cam.draw()
        if gas:

            jet = False

        cam.pos = (player.pos[0] - 250, player.pos[1] - 250)
        if player.pos[1] > 600:
            #player.die()
            pass
        #print(player.vector)
        pygame.display.flip()
        if player.dead:
            pygame.mixer.Sound.play(died_sound)
            done = True
            screen.blit(death, (0, 0))
            pygame.display.flip()
            time.sleep(0.2)
            level2()
        if player.rect.colliderect(endblock.rect):
            done = True
            level3()


def level3():
    player = Player(im, (-1075, 50))
    player.hasjet = True
    level = open("level3.txt", "r")
    blocks = level.read().split("\n")
    cam = Camera(screen, player)
    k = Arrow(270, (-1075, 25), cam)

    endblock = Block((170, 150), (20, 20, 200), (239, 915), cam)

    #endblock = Block()
    rectlist = []
    for item in blocks:
        info = item.split(" ")

        topleft = getint(info[0].split(","))
        dim = getint(info[1].split(","))
        colour = getint(info[2].split(","))

        rectlist.append(Block(dim, colour, topleft, cam))
    llist = [
        Laser((-600, 375), (-830, 280)),
        Laser((170, 670), (170, 550)),
        Laser((345, 670), (345, 550)),
        Laser((481, 550), (481, 365))
    ]
    mid = (-600, 325)
    box = Box(load("box.png", (50, 50)), player, (473, 400), cam)
    rectlist.append(box)
    button = Button(load("upbut.png", (70, 24)), load("downbut.png", (70, 24)),
                    (683, 538), llist[3], cam)
    done = False
    clock = pygame.time.Clock()
    jet = False
    f = 0
    while not done:

        box.update(rectlist, clock.get_time())
        button.update(rectlist, player)

        f -= 0.03
        llist[0].end = (math.sin(f) * 232 + mid[0], 360)
        llist[0].start = (math.sin(f) * 232 + mid[0], 120)
        llist[1].end = (math.sin(-f) * 132 + mid[0] + 332, 360)
        llist[1].start = (math.sin(-f) * 132 + mid[0] + 332, 120)
        llist[2].end = (math.sin(-f) * 132 + mid[0] + 578, 360)
        llist[2].start = (math.sin(-f) * 132 + mid[0] + 578, 120)
        clock.tick(30)
        gas = player.grounded
        pygame.event.pump()
        screen.fill((255, 255, 255))
        for item in llist:

            item.update(player)

        #print(player.rect.collidelist(rectlist))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    jet = True

        player.move(pygame.key.get_pressed(), jet, clock.get_time(), rectlist)

        cam.draw()
        if gas:

            jet = False

        cam.pos = (player.pos[0] - 250, player.pos[1] - 250)
        if player.pos[1] > 600:
            #player.die()
            pass
        #print(player.vector)
        pygame.display.flip()
        if player.dead:
            pygame.mixer.Sound.play(died_sound)
            done = True
            screen.blit(death, (0, 0))
            pygame.display.flip()
            time.sleep(0.2)
            level3()
        if player.rect.colliderect(endblock.rect):
            done = True
            level4()


def level4():
    player = Player(im, (0, 0))
    player.hasjet = True
    player.maxf += 100
    player.fuel = 0
    level = open("level4.txt", "r")
    blocks = level.read().split("\n")
    cam = Camera(screen, player)
    k = Arrow(270, (-1075, 25), cam)

    endblock = Block((132, 250), (20, 20, 200), (-210, 0), cam)
    Arrow(0, (-147, 175), cam)
    #endblock = Block()
    rectlist = []
    for item in blocks:
        info = item.split(" ")

        topleft = getint(info[0].split(","))
        dim = getint(info[1].split(","))
        colour = getint(info[2].split(","))

        rectlist.append(Block(dim, colour, topleft, cam))
    llist = [
        Laser((118, 640), (504, 640)),
        Laser((304, 270), (304, 490)),
        Laser((504, 520), (504, 640)),
        Laser((504, 520), (754, 520)),
        Laser((754, 520), (754, 640)),
        Laser((629, 270), (629, 370)),
        Laser((920, 660), (1135, 650)),
        Laser((300, 670), (300, 1070)),
        Laser((-100, 670), (-100, 1070))
    ]

    done = False
    clock = pygame.time.Clock()
    jet = False
    f = 0
    while not done:
        if player.rect.bottom > 1450:
            pygame.mixer.Sound.play(died_sound)
            player.dead = True

        #button.update(rectlist,player)

        f -= 0.1
        llist[6].end = (math.cos(f)**2 * 215 + llist[6].start[0],
                        math.sin(f) * 415 + llist[6].start[1])
        clock.tick(30)
        gas = player.grounded
        pygame.event.pump()
        screen.fill((255, 255, 255))
        for item in llist:

            item.update(player)

        #print(player.rect.collidelist(rectlist))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    jet = True

        player.move(pygame.key.get_pressed(), jet, clock.get_time(), rectlist)

        cam.draw()
        if gas:

            jet = False

        cam.pos = (player.pos[0] - 250, player.pos[1] - 250)
        if player.pos[1] > 600:
            #player.die()
            pass
        #print(player.vector)
        pygame.display.flip()
        if player.dead:
            pygame.mixer.Sound.play(died_sound)
            done = True
            screen.blit(death, (0, 0))
            pygame.display.flip()
            time.sleep(0.2)
            level4()
        if endblock.rect.colliderect(player.rect):
            level5()
            done = True


def level5():
    player = Player(im, (80, 580))
    player.hasjet = True
    player.fuel = 0
    level = open("level5.txt", "r")
    blocks = level.read().split("\n")
    cam = Camera(screen, player)

    k = Arrow(0, (1715, 800), cam)
    k.image = hsfont.render("more levels coming soon", True, (0, 0, 0))
    #endblock = Block()
    rectlist = []
    for item in blocks:
        info = item.split(" ")

        topleft = getint(info[0].split(","))
        dim = getint(info[1].split(","))
        colour = getint(info[2].split(","))

        rectlist.append(Block(dim, colour, topleft, cam))
    llist = [
        Laser((1420, 55), (1240, 55)),
        Laser((1430, 360), (1675, 360)),
        Laser((1675, 360), (1675, -360)),
        Laser((1185, 350), (1185, 70)),
        Laser((1000, 350), (1000, 70)),
        Laser((560, 360), (795, 360)),
        Laser((335, 200), (1135, 650)),
        Laser((1538, 930), (1538, 760))
    ]

    box = Box(load("box.png", (50, 50)), player, (1080, 0), cam)
    button = Button(load("upbut.png", (70, 24)), load("downbut.png", (70, 24)),
                    (775, 537), llist[5], cam)
    b2 = Button(load("upbut.png", (70, 24)), load("downbut.png", (70, 24)),
                (1430, 906), llist[7], cam)
    rectlist.append(box)
    done = False
    clock = pygame.time.Clock()
    jet = False
    f = 0
    while not done:
        box.update(rectlist, clock.get_time())
        button.update(rectlist, player)
        b2.update(rectlist, player)

        if player.rect.bottom > 1450:
            player.dead = True

        #button.update(rectlist,player)

        f -= clock.get_time() / 200
        llist[6].end = (math.cos(f * -1) * 150 + llist[6].start[0],
                        math.sin(f * -1) * 150 + llist[6].start[1])
        llist[3].start = (llist[3].start[0],
                          math.cos(f / 3)**2 * 280 + llist[3].end[1])
        llist[4].start = (llist[4].start[0],
                          math.cos(f / 2.9)**2 * 280 + llist[4].end[1])
        clock.tick(30)
        gas = player.grounded
        pygame.event.pump()
        screen.fill((255, 255, 255))
        for item in llist:

            item.update(player)

        #print(player.rect.collidelist(rectlist))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    jet = True

        player.move(pygame.key.get_pressed(), jet, clock.get_time(), rectlist)

        cam.draw()
        if gas:

            jet = False

        cam.pos = (player.pos[0] - 250, player.pos[1] - 250)
        if player.pos[1] > 600:
            #player.die()
            pass
        #print(player.vector)
        pygame.display.flip()
        if player.dead:
            pygame.mixer.Sound.play(died_sound)
            done = True
            screen.blit(death, (0, 0))
            pygame.display.flip()
            time.sleep(0.2)
            level5()


level1()

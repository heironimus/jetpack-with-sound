import pygame
import math
from random import uniform, randint

GRAVITY = 0.03
DOWN = math.pi / 2



def clamp(val, maxi, mini):
    return min(maxi, max(val, mini))


def sign(x):
    if x < 0:
        return -1
    else:
        return 1


def sqr(x):
    return x * x


def dist2(v, w):
    return sqr(v[0] - w[0]) + sqr(v[1] - w[1])


def disttosegment(v, w, p):
    l2 = dist2(v, w)
    if l2 == 0:
        return dist2(p, v)
    else:
        t = ((p[0] - v[0]) * (w[0] - v[0]) + (p[1] - v[1]) *
             (w[1] - v[1])) / l2
        t = max((0, min(1, t)))
        return dist2(p,
                     (v[0] + t * (w[0] - v[0]), v[1] + t * (w[1] - v[1])))**0.5


class Camera():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.dlist = []
        self.pos = (0, 0)

    def draw(self):
        self.player.draw(self.screen, self.pos)
        for item in self.dlist:
            self.screen.blit(item.image, (item.rect.topleft[0] - self.pos[0],
                                          item.rect.topleft[1] - self.pos[1]))


class Particle():
    def __init__(self, radius, colour, ltime, dir, speed, pos, plist):
        self.pos = pos
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA,
                                    32)

        pygame.draw.circle(self.image, colour, (radius, radius), radius,
                           radius)
        self.dir = dir
        self.speed = speed
        self.ltime = ltime
        self.maxtime = ltime
        self.plist = plist
        plist.append(self)

    def update(self):

        self.ltime -= 1
        self.pos = (self.pos[0] + math.cos(self.dir) * self.speed,
                    self.pos[1] + math.sin(self.dir) * self.speed)
        self.image.set_alpha(255 * (self.ltime / self.maxtime))
        if self.ltime <= 0:
            self.plist.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.pos))


class Player():
    def __init__(self, image, pos):
        self.image = image
        self.jet_im= pygame.image.load("jetpack.png")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.vector = [0, 0]
        self.acc = 0.15  #pix/milisecond^2
        self.grounded = False
        self.pressed = False
        self.fuel = 1400
        self.maxf = 1400
        self.plist = []
        self.signlm = -1
        self.respawn = pos
        self.dead = False
        self.hasjet = False
        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.jetpack_sound = pygame.mixer.Sound("sounds/jetpack.wav")

      
    def die(self):
        self.vector = [0, 0]
        
        self.dead = True

    def coltest(self, rectlist):
        out = []
        for item in rectlist:
            if self.rect.colliderect(item.rect):
                out.append(item.rect)
        return out

    def colRectify(self, rectlist):

        self.rect.y += self.vector[1]
        tryy = self.coltest(rectlist)

        self.grounded = False
        for item in tryy:
            if self.vector[1] > 0:
                self.rect.bottom = item.top

                self.vector[1] = 0
            elif self.vector[1] < 0:
                self.rect.top = item.bottom
                self.vector[1] = 0

        self.rect.x += self.vector[0]
        tryx = self.coltest(rectlist)
        for item in tryx:
            if self.vector[0] > 0:
                self.rect.right = item.left
                self.vector[0] = 0

            elif self.vector[0] < 0:
                self.rect.left = item.right
                self.vector[0] = 0

        self.pos = self.rect.center
        self.rect.y += 1
        gcheck = self.coltest(rectlist)
        self.rect.y -= 1
        if len(gcheck) > 0:
            self.grounded = True
            self.fuel = self.maxf
            self.pressed = False
    def move(self, keys, jet, deltatime, rectlist):
        if self.pressed and self.fuel > 0:
            self.fuel -= deltatime
        
        self.vector[0] = round(self.vector[0] * 0.5, 0)
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]

        self.vector[0] += self.acc * deltatime * (right - left)
        if right-left!=0:
          self.signlm = right - left
        up = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        if up and self.grounded:
            pygame.mixer.Sound.play(self.jump_sound)
            self.vector[1] -= 16
        elif up and jet and self.fuel > 0 and self.hasjet:
            if pygame.mixer.Sound.get_num_channels(self.jetpack_sound) == 0:
                pygame.mixer.Sound.play(self.jetpack_sound)

            self.vector[1] = -(self.acc * deltatime *2)
            self.pressed = True
            for i in range(3):
                if self.signlm == -1:
                  Particle(randint(3, 7),
                         (randint(190, 255), randint(0, 125), randint(0, 25)),
                         63, uniform(DOWN - 0.4, DOWN + 0.4), 10.8,
                         (self.rect.right+2.5,self.rect.center[1]), self.plist)
                elif self.signlm == 1:
                  Particle(randint(3, 7),
                         (randint(190, 255), randint(0, 125), randint(0, 25)),
                         63, uniform(DOWN - 0.4, DOWN + 0.4), 10.8,
                         (self.rect.left-15,self.rect.center[1]), self.plist)
        if not self.grounded:
            self.vector[1] += GRAVITY * deltatime
        self.vector[1] = clamp(self.vector[1], 18, -100)
        self.colRectify(rectlist)

    def draw(self, screen, campos):

        for item in self.plist:
            screen.blit(item.image, (item.pos[0] - campos[0],
                                     item.pos[1] - campos[1] - item.radius))
            item.update()
        im = pygame.transform.scale(self.image,(self.rect.width,self.rect.height-(self.vector[1]/5)))
        if self.signlm == -1:
          
          im = pygame.transform.flip(im,True,False)
        screen.blit(im, (self.rect.topleft[0] - campos[0],
                                 self.rect.topleft[1] - campos[1]))
        if self.hasjet:
          if self.signlm == -1:
            screen.blit(self.jet_im,(self.rect.topleft[0]-campos[0]+self.rect.width,self.rect.topleft[1]-campos[1]))
          elif self.signlm == 1:
            screen.blit(self.jet_im,(self.rect.topleft[0]-campos[0]-15,self.rect.topleft[1]-campos[1]))

class Block():
    def __init__(self, dim, colour, tl, camera):
        self.image = pygame.Surface(dim)
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft=tl)
        camera.dlist.append(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Arrow():
  def __init__(self,angle,pos,cam):
    self.image = pygame.transform.rotate(pygame.image.load("arrow.png"),angle)
    self.rect = self.image.get_rect(center = pos)
    cam.dlist.append(self)
class Laser():
    def __init__(self, start, end):
        self.buzz_sound = pygame.mixer.Sound("sounds/buzz.wav")

        self.start = start
        self.end = end
        self.length = math.hypot(start[0] - end[0], start[1] - end[1])
        self.angle = math.atan2(start[0] - end[0], start[1] - end[1]) + math.pi
        #print(self.length, self.angle)
        self.pnum = 35
        self.on = True
    def draw(self, player):
        for i in range(self.pnum):
            k = (i / self.pnum) * self.length
            pos = (self.start[0] + math.sin(self.angle) * k,
                   self.start[1] + math.cos(self.angle) * k)
            if abs(pos[0]-player.pos[0])<=250 and abs(pos[1]-player.pos[1])<=250:
              
              if pygame.mixer.Sound.get_num_channels(self.buzz_sound) == 0:
                pygame.mixer.Sound.play(self.buzz_sound)
                pygame.mixer.Sound.set_volume(self.buzz_sound, 0.05)
              Particle(randint(3,5), (0, randint(0, 75), randint(175, 255)), 4,
                     uniform(-math.pi, math.pi), 4, pos, player.plist)

    def colcheck(self, player):
        dist = disttosegment(self.start, self.end, player.rect.center)
        if dist < (player.rect.width ):
            player.die()

    def update(self, player):
      start = self.start
      end = self.end
      self.length = math.hypot(start[0] - end[0], start[1] - end[1])
      self.angle = math.atan2(start[0] - end[0], start[1] - end[1]) + math.pi
      if self.on:
          self.draw(player)
          self.colcheck(player)


class Box:
    def __init__(self, image, player, pos, camera):
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.yvec = 0
        self.xvec = 0
        self.player = player
        self.grounded = False
        camera.dlist.append(self)

    def coltest(self, rectlist):
        out = []
        for item in rectlist:
            if self.rect.colliderect(item.rect):
                out.append(item.rect)
        return out

    def push(self):
        r = self.player.rect
        v = self.player.signlm

        r.x += self.player.signlm * 3
        if len(self.player.coltest([self])) > 0:

            if v > 0:
                self.xvec = 3

            elif v < 0:
                self.xvec = -3

        r.x -= self.player.signlm * 3

    def colrectify(self, rectlist):
        k = rectlist[::-1]
        k.remove(self)
        
        self.rect.y += self.yvec
        for item in self.coltest(k):
            self.rect.bottom = item.top
            self.yvec = 0
        if self.player.rect.top < self.rect.bottom and self.rect.colliderect(self.player.rect):
          self.rect.bottom = self.player.rect.top
          self.grounded = True
          
        self.rect.x += self.xvec
        for item in self.coltest(k):
            if self.xvec < 0:
                self.rect.left = item.right
            elif self.xvec > 0:
                self.rect.right = item.left
        self.grounded = False
        self.rect.y += 1
        if len(self.coltest(k)) > 0 or self.rect.colliderect(self.player.rect):
            self.grounded = True
        self.rect.y -= 1

    def update(self, rectlist, deltatime):

        self.colrectify(rectlist)
        if not self.grounded:
            self.yvec += GRAVITY * deltatime
        else:
            self.yvec = 0
        self.rect.y += self.yvec
        self.push()
        self.xvec = round(self.xvec / 2, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Button():
  def __init__(self,upim,downim,pos,toggle,camera):
    self.upim = upim
    self.downim = downim
    self.image = self.upim
    self.rect = self.upim.get_rect(center = pos)
    self.closed = False
    self.toggle = toggle
    camera.dlist.append(self)
  def update(self,rectlist,player):
    self.closed = False
    for item in rectlist:
      if item.rect.colliderect(self.rect):
        self.closed = True
    if player.rect.colliderect(self.rect):
      self.closed = True
    self.image = self.upim
    self.toggle.on = True
    if self.closed:
      self.image = self.downim
      self.toggle.on = False
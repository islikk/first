from pygame import*
from random import*
from time import time as timer

win_width = 700
win_height = 500

font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

window = display.set_mode((win_width,win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.png"),(win_width,win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")


font.init()
font2 = font.SysFont(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,30,40,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = -50
            self.speed = randint(1,6)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < -10:
            self.kill()

bullets = sprite.Group()


run = True
finish = False

life = 5
score = 0
lost = 0
num_fire = 0
rel_time = False

ship = Player("rocket.png",5, win_height-100, 80,100,10)

listUfoSprite = ["ufo.png","asteroid.png"]
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(listUfoSprite[randint(0,len(listUfoSprite)-1)],randint(80,win_width-80),-50,80,50,randint(1,5))
    monsters.add(monster)

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False


        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if finish != True:
        window.blit(background,(0,0))

        text = font2.render("Рахунок:"+str(score),True,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено:"+str(lost),True,(255,255,255))
        window.blit(text_lose,(10,50))

        ship.reset()
        ship.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...",1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -50, 80, 50, randint(1, 5))
            monsters.add(monster)


        if sprite.spritecollide(ship,monsters,False):
            sprite.spritecollide(ship,monsters,True)
            life -= 1

        if score >= 15:
            finish = True
            window.blit(win,(win_width/2,win_height/2))

        if life < 1 or lost >=15:
            finish = True
            window.blit(lose,(win_width/2-50,win_height/2))

        if life > 3:
            fill_color = (0, 150, 0)
        elif life > 1:
            fill_color = (150, 150, 0)
        else:
            fill_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, fill_color)
        window.blit(text_life, (640, 20))





    display.update()
    time.delay(50)
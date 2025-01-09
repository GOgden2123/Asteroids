import pygame as pg
import random 
from random import randint
from random import randrange 
from math import pi, sin, cos

#global variables
screen = None
screen_size = [800,600]
clock = None
fps = 40
keys_down = []
mouse_buttons = []
mouse_pos = []

#Degrees to Radian function 
def degtoRad(n):
    return (n/360.0) * (pi*2)

#Asteroid Class
class Asteroid:
    def __init__ (self, render_Surface):
        #Position & Movement 
        self.render_Surface = render_Surface
        self.points = []
        self.direction = degtoRad(56)
        self.speed = 1.0

        #Shape of the Asteroid
        self.radius = 50

        #Rendering an Asteroid
        self.color = [255,255,255]
        self.thickness = 3
        self.visual_angle = 0.0

        self.x = randint(0, screen_size[0])
        self.y = randint(0, screen_size[1])
        self.n = 10
        self.polar_cords = []
        self.visible = True 

        #Asteroid screen movement
        for i in range (self.n):
            r = randint(25, 50)
            angle = 2*pi / self.n
            self.polar_cords.append([r, angle*i])
            self.points.append([r*cos(angle*i)+self.x, r*sin(angle*i)+self.y])
                
        return

    def update (self):
        self.points = []
        dx = self.speed*cos(self.direction)
        dy = self.speed*sin(self.direction)
        self.x = dx + self.x
        self.y = dy + self.y
        self.visual_angle +=0.1
        
        #Out of bounds handling
        if self.x > screen_size[0]:
            self.x = 0
        elif self.x < 0:
            self.x = screen_size[0]

        if self.y > screen_size[1]:
            self.y = 0
        elif self.y < 0:
            self.y = screen_size[1]
        
        for i in range (self.n):
            r = self.polar_cords[i][0]
            #Asteroid rotatational movement
            angle = self.polar_cords[i][1]+self.visual_angle
            self.points.append([r*cos(angle)+self.x, r*sin(angle)+self.y])
            
        return

    def render (self):
         if self.visible == True:
             pg.draw.polygon(self.render_Surface,self.color,self.points,self.thickness)
             
         return

    def collide (self, otherThing):
        otherX = 0
        otherY = 1
        try:
            otherX = otherThing.x
            otherY = otherThing.y
        except:
            otherX = otherThing.center[0]
            otherY = otherThing.center[1]
        distance = ((otherX - self.x)**2+(otherY - self.y)**2)**0.5
        radii = self.radius + otherThing.radius
        return distance <= radii

    def resize (self, radius):
        self.polar_cords = []
        self.radius = radius
        angle = 0
        for i in range (self.n):
            r = randint(int (radius * 0.6), int (radius))
            angle = 2*pi / self.n
            self.polar_cords.append([r, angle*i])
            self.points.append([r*cos(angle*i)+self.x, r*sin(angle*i)+self.y])
                
        #end Asteroid class

#Ship Class
class Ship:
    def __init__ (self, render_Surface):
        self.render_Surface = render_Surface
        #self.points = [[150,550],[190,190],[200,190]]
        self.gunBarrel = []
        self.color = [255,255,255]
        self.thickness = 2
        self.shipDirection = 0
        self.speed = 5
        self.r = randint(25, 50)
        #Origin (X,Y) 
        self.x = randint(0, screen_size[0])
        self.y = randint(0, screen_size[1])
        #Stored as angle/radius 
        self.polar_cords = [[0,20], [degtoRad(100),5], [degtoRad(260),5]]
        self.rotation_speed = 5
        self.num_points = 3 
        return

    def update (self):
        #Ship Movement
        if keys_down [pg.K_RIGHT]:
            self.shipDirection += 0.1
        if keys_down [pg.K_UP]:
            dx = self.speed * cos(self.shipDirection)
            dy = self.speed * sin(self.shipDirection)

            self.x += dx
            self.y += dy
        
        if self.x > screen_size[0]:
            self.x = 0
        elif self.x <= -1:
            self.x = screen_size[0]
            
            
            

        if self.y > screen_size[1]:
            self.y = 0
        elif self.y <= -1:
            self.y = screen_size[1]
            
            
            
        if keys_down [pg.K_LEFT]:
            self.shipDirection -= 0.1
        xn = self.polar_cords[0][1]*cos(self.polar_cords[0][0]+self.shipDirection) + self.x
        yn = self.polar_cords[0][1]*sin(self.polar_cords[0][0]+self.shipDirection) + self.y
        self.gunBarrel = [xn,yn]
        return
    
    def render (self):
        points = []
        for i in range (self.num_points):
            xn = self.polar_cords[i][1]*cos(self.polar_cords[i][0]+self.shipDirection) + self.x
            yn = self.polar_cords[i][1]*sin(self.polar_cords[i][0]+self.shipDirection) + self.y
            points.append([xn,yn])
            
        pg.draw.polygon(self.render_Surface,self.color,points,self.thickness)
        return


    def respawn (self):
        return
    #end Ship class

class Bullet:
    def __init__ (self, velocity, render_Surface):
        self.render_Surface = render_Surface
        self.velocity = 1
        self.color = [255,255,255]
        self.center = [1,1]
        self.radius = 3
        self.thickness = 0
        self.direction = 0
        self.readyToFire = True
        self.visible = False
        self.active = True
        return

    def update (self):
        if self.active == True:
            dx = self.velocity*cos(self.direction)
            dy = self.velocity*sin(self.direction)
            self.center[0] = dx + self.center[0]
            self.center[1] = dy + self.center[1]
            #Checking for center going off all sides of screen
            if self.center[0] > screen_size[0]:
                self.readyToFire = True
                self.visible = False
            if self.center[1] > screen_size[1]:
                self.readyToFire = True
                self.visible = False
            if self.center[0] < 0:
                self.readyToFire = True
                self.visible = False
            if self.center[1] < 0:
                self.readyToFire = True
                self.visible = False
                
            
            
        return

    def render (self):
        if self.visible == True:
            pg.draw.circle(self.render_Surface,self.color,self.center,self.radius,self.thickness)
        
        return

    def shoot (self, speed, direction, startPosition):
        if self.readyToFire == True:
            self.center = startPosition
            self.direction = direction
            self.velocity = speed
            self.readyToFire = False
            self.visible = True
            self.active = True 
        return
        #end while 

    #end Bullet class

class explosion:
    def __init__ (self, render_Surface, x, y):
        self.render_Surface = render_Surface
        self.x = x
        self.y = y
        self.particles = []
        for i in range (10):
            self.particles.append(Bullet(randint(5,10), render_Surface))
            self.particles[i].radius = 1
            self.direction = degtoRad(randint(0,360))
            #end for


            
            
        return

    def render (self):
        for particle in self.particles:
            particle.render()

        return

    def update(self):
        for particle in self.particles:
            particle.update()

        return 

    def detonate (self):
        for particle in self.particles:
            #Put all particles into one point
            particle.center = [1,1]
            #Give every particle a random speed and direction
            particle.velocity = random.randint(1,5)
            particle.direction = degtoRad(random.randint(0,360))
            #Give every particle a random duration
            #particle.duration = random.randint(1,6)

            return

        return 
        
    #end explosion class
        
            
def main():
    global keys_down
    #initialize Pygame
    pg.init()
    
    #assign a display surface to our screen
    screen = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()    
    num_asteroids = []
    ship = Ship(screen)
    bullet = Bullet(1, screen)
    for i in range (2):
        num_asteroids.append(Asteroid(screen))
        num_asteroids[-1].direction = degtoRad(randint(0,359))
        
    #create main game loop
    running = True

    while running:
        #handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            #end if
        #end for

        #get keys pressed
        keys_down = pg.key.get_pressed()
        #Firing a bullet
        if keys_down[pg.K_SPACE]:
            bullet.shoot(5, ship.shipDirection, ship.gunBarrel)

        #get mouse position
        mouse_pos = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed()
        

        #sync frame rate
        clock.tick(fps)
        
        #update game objects
        for i in num_asteroids:
            i.update()

        ship.update()
        bullet.update()
        
        
        #Bullet collision with asteroid 
        #What do we want to happen? When a bullet is shot, we want to see it collide with an asteroid and break it into two smaller asteroids (two new instances?).
        #To reflect this we would want to remove an asteroid from num_asteroids list and add a smaller asteroid in.
        #Splitting normal asteroid into two smaller asteroids upon collision
        new_asteroids = []
        deleted_asteroids = []

        for i in range(len(num_asteroids)):
            if num_asteroids[i].collide(bullet):
                bullet.center[0] = 10000
                deleted_asteroids.append(i)

                new_asteroids.append(Asteroid(screen))
                new_asteroids[-1].resize(num_asteroids[i].radius/2)
                print(new_asteroids[-1].radius)
                new_asteroids[-1].x = num_asteroids[i].x
                new_asteroids[-1].x -= 10 
                new_asteroids[-1].y = num_asteroids[i].y
                new_asteroids[-1].y -= 10
                new_asteroids[-1].direction = bullet.direction + degtoRad(30)

                new_asteroids.append(Asteroid(screen))
                new_asteroids[-1].resize(num_asteroids[i].radius/2)
                new_asteroids[-1].x = num_asteroids[i].x
                new_asteroids[-1].x -= 10 
                new_asteroids[-1].y = num_asteroids[i].y
                new_asteroids[-1].y -= 10
                new_asteroids[-1].direction = bullet.direction + degtoRad(-30)
                
        num_asteroids.extend(new_asteroids)

        for i in range (len(num_asteroids)):
            if num_asteroids[i].radius <= 13:
                if i not in deleted_asteroids: 
                    deleted_asteroids.append(i)
        deleted_asteroids = sorted(deleted_asteroids, reverse = True)        
        for i in deleted_asteroids:
            num_asteroids.pop(i)

        #render screen
        screen.fill((0,0,0))
        ship.render()
        bullet.render()

        for i in range(len(num_asteroids)):
            num_asteroids[i].render()
            
        pg.display.flip()
    #end while

    pg.quit()

    return
#end main

#module guard
if __name__ == '__main__':
    #run this file's main function
    main()
#end if

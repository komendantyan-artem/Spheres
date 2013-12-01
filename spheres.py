import math
import random

class Sphere:
    def __init__(self, x, y, radius, Vx=0, Vy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.Vx = Vx
        self.Vy = Vy
    
    def motion(self):
        self.x += self.Vx
        self.y += self.Vy
        distance = math.sqrt(self.x ** 2 + self.y ** 2) + self.radius
        if distance > world.radius:
            self.radius -= distance - world.radius
    
    def jet(self, direction):
        pass

def collision(sphere1, sphere2):
    '''
    d - расстояние между центрами окружностей.
    S = R1**2 + R2**2
    Получаем систему уравнений. x, y - новые радиусы.
    x + y = d
    x**2 + y**2 = S   (сократили на пи обе части уравнения)
    Решаем.
    Если y < 0, то произошло полное поглощение. Тогда y = 0, пересчитываем x:
    x = sqrt(S)
    '''
    
    R1, R2 = sphere1.x, sphere2.x
    d = math.sqrt((sphere1.x - sphere2.x)**2 + (sphere1.y - sphere2.y)**2)
    if d >= R1 + R2: return
    S = R1**2 + R2**2
    
    y = (d - math.sqrt(2*S - d**2))/2
    if y < 0:
        y = 0
        x = math.sqrt(S)
    else:
        x = (d + math.sqrt(2*S - d**2))/2
    
    if R1 > R2 or R1 == R2 and random.getrandbits(1):
        newR1, newR2 = x, y
    else:
        newR1, newR2 = y, x
    
    '''
    Теперь нужно пересчитать скорости обоих тел из закона сохранения импульса.
    Скорее всего, принцип, по которому я пересчитываю скорости неправилен.
    Но он может быть неправилен в меру (и когда-нибудь это можно будет поправить).
    Плотности везде сокращаются, поэтому я беру площади тел.
    '''
    
    Vx1, Vx2 = sphere1.Vx, sphere2.Vx
    S1, S2 = R1**2, R2**2
    newS1 = newR1**2
    newS2 = newR2**2
    if newR1 != 0: newVx1 = (S1 * Vx1 + S2 * Vx2) / newS1
    else:          newVx1 = 0
    if newR2 != 0: newVx2 = (S1 * Vx1 + S2 * Vx2) / newS2
    else:          newVx2 = 0
    
    Vy1, Vy2 = sphere1.Vy, sphere2.Vy
    if newR1 != 0: newVy1 = (S1 * Vy1 + S2 * Vy2) / newS1
    else:          newVy1 = 0
    if newR2 != 0: newVy2 = (S1 * Vy1 + S2 * Vy2) / newS2
    else:          newVy2 = 0
    
    '''
    Пока что будем сразу пересчитывать параметры, обнаружив столкновение.
    Это точно не будет работать, когда тело столкнулось сразу с несколькими телами.
    В этих случаях нужно сохранять изменения и применять их после обнаружения всех столкновений.
    Но это я сделаю позже.
    '''
    
    sphere1.radius = newR1
    '''sphere1.Vx = newVx1
    sphere1.Vy = newVy1'''
    sphere2.radius = newR2
    '''sphere2.Vx = newVx2
    sphere2.Vy = newVy2'''


class World:
    def __init__(self, radius):
        self.radius = radius
        self.spheres = []
        self.number_of_move = 0
    
    def random_init(self):
        self.radius = 300
        for i in range(100):
            x = random.randrange(-100, 100)
            y = random.randrange(-100, 100)
            radius = random.randrange(1, 50)
            Vx = random.randrange(-3, 4)
            Vy = random.randrange(-3, 4)
            self.spheres.append(Sphere(x, y, radius, Vx, Vy))
    
    def update(self):
        self.number_of_move += 1
        for i in self.spheres:
            i.motion()
        for i in range(len(self.spheres)):
            for j in range(i + 1, len(self.spheres)):
                collision(self.spheres[i], self.spheres[j])
        
        self.spheres = [i for i in self.spheres if i.radius > 0]


world = World(None)
world.random_init()

def rendering(color):
    for i in world.spheres:
        x0 = int(CENTER_OF_WORLD + i.x - i.radius)
        y0 = int(CENTER_OF_WORLD + i.y - i.radius)
        x1 = int(CENTER_OF_WORLD + i.x + i.radius)
        y1 = int(CENTER_OF_WORLD + i.y + i.radius)
        GUI.create_oval(x0, y0, x1, y1, outline=color)

def main():
    root.after(50, main)
    rendering(BACKGROUND)
    world.update()
    rendering(COLOR_OF_SPHERE)

CENTER_OF_WORLD = world.radius + 1
from tkinter import *
BACKGROUND = "white"
COLOR_OF_SPHERE = "blue"
root = Tk()
GUI = Canvas(root, width=world.radius*2 + 2, height=world.radius*2 + 2)
GUI.pack()
GUI.create_oval(2, 2, world.radius*2, world.radius*2, fill=BACKGROUND)

root.after_idle(main)
root.mainloop()
 

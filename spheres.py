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
    
    def jet(self, direction):
        pass

def collision(i, j):
    sphere1, sphere2 = world.spheres[i], world.spheres[j]
    
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
    
    R1, R2 = sphere1.radius, sphere2.radius
    d = math.sqrt((sphere1.x - sphere2.x)**2 + (sphere1.y - sphere2.y)**2)
    if d >= R1 + R2: return
    S1, S2 = R1 ** 2, R2 ** 2
    S = S1 + S2
    
    y = (d - math.sqrt(2*S - d**2))/2
    if y < 0:
        y = 0
        x = math.sqrt(S)
    else:
        x = (d + math.sqrt(2*S - d**2))/2
    
    '''
    Абсолютно упругий или неупругий удары не подходят.
    От балды я полагаю, что скорость меньшего тела не изменится,
        и считаю скорость большего тела из закона сохранения импульса.
    Плотности везде сокращаются, поэтому я беру площади тел.
    '''
    
    Vx1, Vx2 = sphere1.Vx, sphere2.Vx
    Vy1, Vy2 = sphere1.Vy, sphere2.Vy
    
    if R1 > R2 or R1 == R2 and random.getrandbits(1):
        newR1, newR2 = x, y
        diffS = abs(S1 - newR1**2)
        newVx1 = (diffS * Vx2 + S1 * Vx1) / (newR1**2)
        newVy1 = (diffS * Vy2 + S1 * Vy1) / (newR1**2)
        world.changes[i][1] += newVx1 - Vx1
        world.changes[i][2] += newVy1 - Vy1
    else:
        newR1, newR2 = y, x
        diffS = abs(S1 - newR1**2)
        newVx2 = (diffS * Vx1 + S2 * Vx2) / (newR2**2)
        newVy2 = (diffS * Vy1 + S2 * Vy2) / (newR2**2)
        world.changes[j][1] += newVx2 - Vx2
        world.changes[j][2] += newVy2 - Vy2
    
    world.changes[i][0] += newR1 - R1
    world.changes[j][0] += newR2 - R2

def collision_with_border(i):
    sphere = world.spheres[i]
    distance = math.sqrt(sphere.x ** 2 + sphere.y ** 2) + sphere.radius
    if distance > world.radius:
        world.changes[i][0] = world.radius - distance


class World:
    def __init__(self, radius):
        self.radius = radius
        self.spheres = []
        self.changes = None
    
    def random_init(self):
        self.radius = 400
        for i in range(600):
            x = random.randrange(-400, 400)
            y = random.randrange(-400, 400)
            radius = random.randrange(1, 15)
            Vx = random.randrange(-4, 5)
            Vy = random.randrange(-4, 5)
            self.spheres.append(Sphere(x, y, radius, Vx, Vy))
    
    def update(self):
        self.changes = [[0, 0, 0] for i in range(len(self.spheres))]
        self.spheres.sort(key=lambda s: s.x - s.radius)
        for i in self.spheres:
            i.motion()
        for i in range(len(self.spheres)):
            sphere1 = self.spheres[i]
            collision_with_border(i)
            for j in range(i + 1, len(self.spheres)):
                sphere2 = self.spheres[j]
                if sphere2.x - sphere1.x > sphere1.radius + sphere2.radius:
                    break
                collision(i, j)
        self.apply_changes()
     
    def apply_changes(self):
        for i in range(len(self.spheres)):
            sphere = self.spheres[i]
            change = self.changes[i]
            sphere.radius += change[0]
            sphere.Vx     += change[1]
            sphere.Vy     += change[2]
        self.spheres = [i for i in self.spheres if i.radius >= 1]


world = World(None)
world.random_init()

from tkinter import *

def rendering(color="blue"):
    for i in world.spheres:
        x0 = int(CENTER_OF_WORLD + i.x - i.radius)
        y0 = int(CENTER_OF_WORLD + i.y - i.radius)
        x1 = int(CENTER_OF_WORLD + i.x + i.radius)
        y1 = int(CENTER_OF_WORLD + i.y + i.radius)
        GUI.create_oval(x0, y0, x1, y1, outline=color)

def main():
    GUI.delete(ALL)
    GUI.create_oval(0, 0, world.radius*2, world.radius*2, fill="white")
    world.update()
    rendering()
    GUI.update()
    root.after(50, main)

CENTER_OF_WORLD = world.radius + 1
root = Tk()
GUI = Canvas(root, width=world.radius*2 + 2, height=world.radius*2 + 2)
GUI.pack()

root.after_idle(main)
root.mainloop()

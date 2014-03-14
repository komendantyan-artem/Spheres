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

class Change:
    def __init__(self):
        self.radius = self.Vx = self.Vy = 0

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
        x = d - y
    
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
        world.changes[i].Vx += newVx1 - Vx1
        world.changes[i].Vy += newVy1 - Vy1
    else:
        newR1, newR2 = y, x
        diffS = abs(S1 - newR1**2)
        newVx2 = (diffS * Vx1 + S2 * Vx2) / (newR2**2)
        newVy2 = (diffS * Vy1 + S2 * Vy2) / (newR2**2)
        world.changes[j].Vx += newVx2 - Vx2
        world.changes[j].Vy += newVy2 - Vy2
    
    world.changes[i].radius += newR1 - R1
    world.changes[j].radius += newR2 - R2

def collision_with_border(sphere):
    if(sphere.x + sphere.radius > world.width and sphere.Vx > 0 or
       sphere.x - sphere.radius < 0 and sphere.Vx < 0):
        sphere.Vx *= -1
    if(sphere.y + sphere.radius > world.height and sphere.Vy > 0 or
       sphere.y - sphere.radius < 0 and sphere.Vy < 0):
        sphere.Vy *= -1


class World:
    def __init__(self):
        self.radius = 0
        self.spheres = []
        self.changes = None
        self.me = None
    
    def random_init(self, width=700, height=400, max_radius=10, max_velocity_on_axe=4):
        self.width = 700
        self.height = 400
        for i in range(300):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            radius = random.randrange(1, max_radius)
            Vx = random.randrange(-max_velocity_on_axe, max_velocity_on_axe + 1)
            Vy = random.randrange(-max_velocity_on_axe, max_velocity_on_axe + 1)
            self.spheres.append(Sphere(x, y, radius, Vx, Vy))
        self.me = self.spheres[0]
        self.me.radius = random.randrange(max_radius, max_radius + 2)
    
    def update(self):
        for i in self.spheres:
            i.motion()
            collision_with_border(i)
        self.changes = [Change() for i in range(len(self.spheres))]
        self.spheres.sort(key=lambda s: s.x - s.radius)
        for i in range(len(self.spheres)):
            sphere1 = self.spheres[i]
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
            sphere.radius += change.radius
            sphere.Vx     += change.Vx
            sphere.Vy     += change.Vy
        self.spheres = [i for i in self.spheres if i.radius >= 1]
    
    def jet(self, sphere, x, y):
        if sphere.radius < 1:
            return
        
        V_begin = 15
        #S1 + S2 = S => newR**2 + r**2 = R**2
        R = sphere.radius
        newR = 0.98 * R
        r = 0.199 * R
        
        if sphere.y == y and sphere.x == x:
            return
        
        angle = math.atan2(sphere.y - y, sphere.x - x)
        v_x = -V_begin * math.cos(angle)
        v_y = -V_begin * math.sin(angle)
        
        sphere.Vx = (R ** 2 * sphere.Vx - r ** 2 * v_x) / newR ** 2
        sphere.Vy = (R ** 2 * sphere.Vy - r ** 2 * v_y) / newR ** 2
        sphere.radius = newR;
        
        x = sphere.x - (newR + r) * math.cos(angle)
        y = sphere.y - (newR + r) * math.sin(angle)
        
        self.spheres.append(Sphere(x, y, r, v_x, v_y))


world = World()
world.random_init()

from tkinter import *

def rendering():
    graphic.delete(ALL)
    graphic.create_rectangle(2, 2, world.width + 2, world.height + 2, fill="white")
    for i in world.spheres:
        x0 = int(i.x - i.radius)
        y0 = int(i.y - i.radius)
        x1 = int(i.x + i.radius)
        y1 = int(i.y + i.radius)
        color = "blue" if i.radius < world.me.radius else "red"
        graphic.create_oval(x0, y0, x1, y1, outline=color)
    if world.me.radius >= 1:
        x0 = int(world.me.x - world.me.radius)
        y0 = int(world.me.y - world.me.radius)
        x1 = int(world.me.x + world.me.radius)
        y1 = int(world.me.y + world.me.radius)
        graphic.create_oval(x0, y0, x1, y1, outline="green")
    graphic.update()
    

def main():
    world.update()
    rendering()
    root.after(50, main)

root = Tk()
graphic = Canvas(root, width=world.width + 2, height=world.height + 2)
graphic.bind('<ButtonPress-1>', lambda event: world.jet(world.me, event.x, event.y))
graphic.pack()

root.after_idle(main)
root.mainloop()

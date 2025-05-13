from enum import nonmember

from backwork.Vector2D import Vector2D, math
from random import randint
from tkinter import Tk, Canvas

window=Tk()
cont = True
def end(_):
    global cont
    cont = False

window.bind('<Escape>', end)
cnv = Canvas(window, width = 800, height = 600, bg='white')
cnv.place(x=5,y=5)
window.geometry(str(800+10)+'x'+str(600+10))
nb_boids = 125
boids = [(randint(0,360), Vector2D(randint(0, 800), randint(0,600)), cnv.create_oval(0,0,0,0)) for _ in range(nb_boids)]
boids_Head = [cnv.create_oval(0,0,0,0) for _ in range(nb_boids)]
boids_speed = [1 for _ in range(nb_boids)]

def comportment(bird_index:int, bird_list:list[tuple[float, Vector2D, int]], boids_speeds:list[float] = boids_speed)->Vector2D:
    nearest:tuple[float, Vector2D]|None = None
    near = None
    bird = bird_list[bird_index]

    walk_f = Vector2D.from_exp(bird[0] * math.pi / 180, boids_speeds[bird_index])

    boids_speeds[bird_index] += (randint(-10, 10) + randint(-10, 10)) / 20
    if boids_speeds[bird_index] < 0.5:
        boids_speeds[bird_index] = 0.5

    boids_speeds[bird_index] *= 0.995

    angle = bird[0]

    #on le fait bouger, tant qu'à avoir calculé le vecteur de mouvement
    pos = bird[1] + walk_f
    pos.x = (pos.x + 800) % 800
    pos.y = (pos.y + 600) % 600

    bird = bird[0], pos, bird[2]
    bird_list[bird_index] = bird

    for i, b in enumerate(bird_list):
        if i!=bird_index:
            dist = (b[1] - bird[1]).squareNorm()
            if nearest is None:
                nearest = b
                near = dist
            elif near > (b[1] - bird[1]).squareNorm():
                nearest = b
                near = dist

    if near is None:
        return walk_f

    angle += randint(-2,3)
    if near < 64:
        side = walk_f.normal_scalar(nearest[1] - bird[1])
        if side > 0 :
            bird_list[bird_index] = angle+15, bird[1], bird[2]
        else:
            bird_list[bird_index] = angle-15, bird[1], bird[2]
        return walk_f
    if near > 1024:
        side = walk_f.normal_scalar(nearest[1] - bird[1])
        if side < 0 :
            bird_list[bird_index] = angle+5, bird[1], bird[2]
        else:
            bird_list[bird_index] = angle-5, bird[1], bird[2]
        return walk_f
    if nearest[0]>bird[0]:
        bird_list[bird_index] = angle+4, bird[1], bird[2]
    else:
        bird_list[bird_index] = angle-4, bird[1], bird[2]
    return walk_f
while cont:
    for i,j in enumerate(boids):
        n = j[1] + (comportment(i, boids) * 2.5)
        cnv.coords(boids_Head[i], n.x + 3, n.y + 3, n.x-3, n.y-3)
    for b in boids:
        cnv.coords(b[2], b[1].x + 5, b[1].y + 5, b[1].x-5, b[1].y-5)
    cnv.update()

cnv.update()
cnv.destroy()
window.destroy()
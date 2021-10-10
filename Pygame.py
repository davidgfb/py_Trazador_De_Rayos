from math import pi

from numpy import array 
from numpy.linalg import norm

from pygame import init, QUIT, quit
from pygame.display import set_mode, update
from pygame.gfxdraw import pixel
from pygame.event import get

def cero(self = None):
    return Intersection(CERO, -1, CERO, self)

def normaliza(a):
    return a / norm(a)

def y_Recta(m, x, n): # y = m * x + n
    return m * x + n

class Sphere():
    def __init__(self, center, radius, color):
        self.c = center
        self.r = radius
        self.col = color
   
    def intersection(self, l):
        a = l.o - self.c
        b = l.d @ a
        q, i = -a @ a + b ** 2 + self.r ** 2, cero(self)

        if q >= 0:
            d, b = -b, q ** 0.5
            d1, d2 = d - b, d + b
            c, d = y_Recta(l.d, d1, l.o), y_Recta(l.d, d2, l.o)

            if 0 < d1 and (d1 < d2 or d2 < 0):
                i = Intersection(c, d1, self.normal(c), self)

            elif 0 < d2 and (d2 < d1 or d1 < 0):
                i = Intersection(d, d2, self.normal(d), self)

            else:
                i = cero(self)

        return i

    def normal(self, b):
        return normaliza(b - self.c)

class Plane():
    def __init__(self, point, normal, color):
        self.n = normal
        self.p = point
        self.col = color

    def intersection(self, l):
        d, i = l.d @ self.n, cero(self)

        if d != 0:
            d = (self.p - l.o) @ self.n / d
            i = Intersection(y_Recta(l.d, d, l.o), d, self.n, self)

        return i

class Ray():
    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction

class Intersection():
    def __init__(self, point, distance, normal, obj):
        self.p = point
        self.d = distance
        self.n = normal
        self.obj = obj

def testRay(ray, objects, ignore = None):
    intersect = cero()

    for obj in objects:
        if obj != ignore:
            currentIntersect = obj.intersection(ray)

            if currentIntersect.d > 0 and intersect.d < 0 or\
               0 < currentIntersect.d < intersect.d:
                intersect = currentIntersect

    return intersect

def trace(ray, objects, light, maxRecur):
    col = None
    intersect = testRay(ray, objects)
    a = light - intersect.p
    
    if maxRecur < 0:
        col = CERO
    
    if intersect.d == -1:
        col = array(tuple(3 * [AMBIENT]))

    elif intersect.n @ a < 0:
        col = intersect.obj.col * AMBIENT

    else:    
        lightRay, lightIntensity =\
                  Ray(intersect.p, normaliza(a)),\
                  250 / (pi * norm(light - intersect.p) ** 2)                       
        maxi = max(normaliza(intersect.n) @\
                   (normaliza(light - intersect.p) *\
                    lightIntensity), AMBIENT)
        col = intersect.obj.col * maxi

        if testRay(lightRay, objects, intersect.obj).d != -1 and\
           maxi != AMBIENT:
            col = intersect.obj.col * AMBIENT

    return col

def gammaCorrection(color, factor):     
    return tuple((255 ** (1 - factor) * color ** factor)\
                 .astype(int))   

def renderiza():
    for x in r:  
        for y in r:  
            a = array((x, y, 0)) - 250 * XY - 50 * cameraPos
            ray = Ray(cameraPos, normaliza(a))
            col = trace(ray, objs, lightSource, 10)
            v = array((x, -y)) + (dim - 1) * Y[:2]
            x, y = v

            pixel(PANTALLA, x, y,\
                  gammaCorrection(col, GAMMA_CORRECTION))

    update()
    print("ya")

def ciclaJuego():
    while True: 
        for event in get():
            if event.type == QUIT:
                quit()
                exit()

CERO, X, Y, Z = array((0, 0, 0)), array((1, 0, 0)),\
                array((0, 1, 0)), array((0, 0, 1))
XY = X + Y
XYZ, dim = XY + Z, 500 # dim = fov

AMBIENT, GAMMA_CORRECTION, objs, lightSource, cameraPos, r =\
         0.1, 0.45, (Sphere(-2 * array((1, 0, 5)), 2, 255 * Y),\
        Sphere(2 * array((1, 0, -5)), 3.5, 255 * X),\
        Sphere(-array((0, 4, 10)), 3, 255 * Z),\
        Plane(-12 * Z, Z, 255 * XYZ)), -10 * X,\
        20 * Z, range(dim)

PANTALLA = set_mode((dim, dim))

init()
		
renderiza()
ciclaJuego()

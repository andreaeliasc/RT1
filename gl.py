import struct
import math
import time
from random import randint as random
from random import uniform as randomDec
from obj import ObjReader
from arithmetics import *

def char(c):
    '''1 Byte'''

    return struct.pack('=c', c.encode('ascii'))

def word(w):
    '''2 Bytes'''

    return struct.pack('=h', w)

def dword(d):
    '''4 Bytes'''

    return struct.pack('=l', d)

def color(r,g,b):
    '''Set pixel color'''

    return bytes([b , g , r ])

def barycentric(A, B, C, P):
    '''Convert vertices to barycentric coordinates'''
    
    cx, cy, cz = cross(V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y))

    #CZ Cannot be less 1
    if cz == 0:
        return -1, -1, -1

    #Calculate the barycentric coordinates
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    return  w, v, u

BLACK = color(0,0,0)
WHITE = color(255,255,255)
PI = 3.14159265359

class Raytracer(object):
    '''Raytracer Class'''

    def __init__(self, width, height):
        '''Constructor'''

        self.current_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

        self.camPosition = V3(0, 0, 0)
        self.fov = 60

        self.scene = []

    def glInit(self):
        '''Initialize any internal objects that your renderer software requires'''

        pass

    def glCreateWindow(self, width, height):
        '''Initialize framebuffer, img will be this size'''

        self.height = height
        self.width = width
        self.glClear()
        self.glViewPort(0, 0, width, height)
    
    def glViewPort(self, x, y, width, height):
        '''Define the area of the image to draw on'''

        self.x = x
        self.y = y
        self.vpx = width
        self.vpy = height

    def glClear(self):
        '''Set all pixels to same color'''

        self.framebuffer = [
            [
                self.clear_color for x in range(self.width)
                ]
            for y in range(self.height)
        ]

        self.zbuffer = [
            [
                float('inf') for x in range(self.width)
                ]
            for y in range(self.height)
        ]

    def glBackground(self, texture):
        '''Background'''

        self.framebuffer = [ [ texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in range(self.height) ]

    def glVertex(self, x, y, color = None):
        '''Change the color of a point on the screen. The x, y coordinates are 
        specific to the viewport that they defined with glViewPort().'''

        pixelX = ( x + 1) * (self.vpx  / 2 ) + self.x
        pixelY = ( y + 1) * (self.vpy / 2 ) + self.y

        if pixelX >= self.width or pixelX < 0 or pixelY >= self.height or pixelY < 0:
            return

        try:
            self.framebuffer[round(pixelY)][round(pixelX)] = color or self.current_color
        except:
            pass

    def glVertex_coord(self, x, y, color = None):
        if x < self.x or x >= self.x + self.vpx or y < self.y or y >= self.y + self.vpy:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.framebuffer[y][x] = color or self.current_color
        except:
            pass

    def glColor(self, r, g, b):
        '''Change the color glVertex() works with. The parameters must 
        be numbers in the range of 0 to 1.'''

        try:
            self.rv = round(255*r)
            self.gv = round(255*g)
            self.bv = round(255*b)
            self.vertex_color = color(self.rv,self.gv,self.bv)
        except ValueError:
                print('\nERROR: Please enter a number between 1 and 0\n')

    def glClearColor(self, r, g, b):
        '''Can change the color of glClear(), parameters must be numbers in the 
        range of 0 to 1.'''

        try:
            self.rc = round(255*r)
            self.gc = round(255*g)
            self.bc = round(255*b)
            self.clear_color = color(self.rc, self.gc, self.bc)
        except ValueError:
            print('\nERROR: Please enter a number between 1 and 0\n')

    def glFinish(self, file_name):
        '''Write Bitmap File'''
        
        bmp_file = open(file_name, 'wb')

        #File header 14 bytes
        bmp_file.write(char('B'))
        bmp_file.write(char('M'))
        bmp_file.write(dword(14 + 40 + self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(14 + 40))
        
        #File info 40 bytes
        bmp_file.write(dword(40))
        bmp_file.write(dword(self.width))
        bmp_file.write(dword(self.height))
        bmp_file.write(word(1))
        bmp_file.write(word(24))
        bmp_file.write(dword(0))
        bmp_file.write(dword(self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))

        # Pixeles, 3 bytes each
        for x in range(self.height):
            for y in range(self.width):
                bmp_file.write(self.framebuffer[x][y])
            
        bmp_file.close()

    def glZBuffer(self, filename):
        bmp_file = open(filename, 'wb')

        # File header 14 bytes
        bmp_file.write(bytes('B'.encode('ascii')))
        bmp_file.write(bytes('M'.encode('ascii')))
        bmp_file.write(dword(14 + 40 + self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(14 + 40))

        # Image Header 40 bytes
        bmp_file.write(dword(40))
        bmp_file.write(dword(self.width))
        bmp_file.write(dword(self.height))
        bmp_file.write(word(1))
        bmp_file.write(word(24))
        bmp_file.write(dword(0))
        bmp_file.write(dword(self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                bmp_file.write(color(depth,depth,depth))

        bmp_file.close()

    def rtRender(self):
        for y in range(self.height):
            for x in range(self.width):
                # NDC
                Px = 2 * ( (x+0.5) / self.width) - 1
                Py = 2 * ( (y+0.5) / self.height) - 1

                # FOV
                t = math.tan( (self.fov * PI / 180) / 2 )
                r = t * self.width / self.height
                Px *= r
                Py *= t

                # Cam always towards -k
                direction = V3(Px, Py, -1)
                direction = div(direction, magnitud(direction))

                material = None

                for obj in self.scene:
                    intersect = obj.ray_intersect(self.camPosition, direction)
                    if intersect is not None:
                        if intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = intersect.distance
                            material = obj.material

                if material is not None:
                    self.glVertex_coord(x, y, material.diffuse)

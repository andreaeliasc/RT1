import collections

#Constants
V2 = collections.namedtuple('Point2', ['x', 'y'])
V3 = collections.namedtuple('Point3', ['x', 'y', 'z'])
V4 = collections.namedtuple('Point4', ['x', 'y', 'z', 'w'])

def sum(v0, v1):
    '''Vector Sum'''
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
    '''Vector Substraction'''
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
    '''Vector Multiplication'''
    return V3(v0.x * k, v0.y * k, v0.z * k)

def div(v0, k):
    '''Vector Divition'''
    return V3(v0.x / k, v0.y / k, v0.z / k)

def dot(v0, v1):
    '''Dot Product'''
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
    '''Cross Product'''
    
    x = v0.y * v1.z - v0.z * v1.y
    y = v0.z * v1.x - v0.x * v1.z
    z = v0.x * v1.y - v0.y * v1.x

    return V3(x, y, z)

def magnitud(v0):
    '''Vector Magnitud'''
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    '''Normal vector'''
    l = magnitud(v0)
    if l == 0:
        return V3(0, 0, 0)
    else:
        return V3(v0.x/l, v0.y/l, v0.z/l)

def multMatrices(m1,m2):
    '''Multiply Matrices'''

    if len(m1[0]) == len(m2):
        resultMatrix = [[0] * len(m2[0]) for i in range(len(m1))]
        for x in range(len(m1)):
            for y in range(len(m2[0])):
                for z in range(len(m1[0])):
                    try:
                        resultMatrix[x][y] += m1[x][z] * m2[z][y]
                    except IndexError:
                        pass
        return resultMatrix
    else:
        print("\nERROR: The matrix multiplication could not be done because the number of columns of the first matrix is not equal to the number of rows of the second matrix")
        return 0

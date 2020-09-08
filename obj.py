class ObjReader(object):
    '''Obj File Reader'''
    
    def __init__(self, filename, mtl = None):
        '''Constructor'''
        self.verifier = False
        #Open and read .obj file
        with open(filename) as obj_file:
            self.lines = obj_file.read().splitlines()
        
        if mtl:
            self.verifier = True
            with open(mtl) as x:
                self.lines2 = x.read().splitlines()
        
        self.vertices = []
        self.normals = []
        self.tex_coords = []
        self.faces = []

        self.matType = []
        self.kD = []

        self.material = {}

        #Reads individual lines from .obj file
        self.readLines()
    

    def removeSpaces(self, face):
        '''Remove empty spaces if they exist'''

        store_data = face.split('/')

        if ("") in store_data:
            store_data[1] = 0
        
        return map(int, store_data)

    def readLines(self):
        '''Read individual lines from .obj file'''

        if self.verifier:
            for line2 in self.lines2:
                if line2:
                    prefix2, value2 = line2.split(' ', 1)
                    if prefix2 == 'newmtl':
                        self.matType.append(value2)
                    if prefix2 == 'Kd':
                        self.kD.append(list(map(float,value2.split(' '))))
            for index in range(len(self.matType)-1):
                self.material[self.matType[index]] = self.kD[index]
        
        self.mater = ""

        for line in self.lines:        
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float,value.split(' '))))
                if prefix == 'vn':
                    self.normals.append(list(map(float,value.split(' '))))
                if prefix == 'vt':
                    self.tex_coords.append(list(map(float,value.split(' '))))
                if prefix == 'f':
                    if self.verifier:
                        listita = [list(self.removeSpaces(face)) for face in value.split(' ')]
                        listita.append(self.mater)
                        self.faces.append(listita)
                    else:
                        self.faces.append([list(self.removeSpaces(face)) for face in value.split(' ')])
                if prefix == 'usemtl':
                    self.mater = value

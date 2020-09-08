from gl import *
from texture import Texture
from obj import ObjReader
from sphere import Sphere, Material

if __name__ == '__main__':
    '''Main Program'''

    snow = Material(diffuse = color(224, 224, 224))
    buttons = Material(diffuse = color(112, 112, 112 ))
    smile = Material(diffuse = color(0, 0, 0))
    carrot = Material(diffuse = color(255, 92, 57))
    eye = Material(diffuse = color(153, 153, 153))


    width = 500
    height = 300
    r = Raytracer(width,height)

    # BODY
    r.scene.append( Sphere(V3(0, 0.80, -5), 0.60, snow) ) #HEAD
    r.scene.append( Sphere(V3(0, 0,  -5), 0.75, snow) ) # BELLY
    r.scene.append( Sphere(V3(0, -1, -5), 1, snow) ) # LEGS

    # Buttons
    r.scene.append( Sphere(V3(0, 0, -2), 0.05, buttons) )
    r.scene.append( Sphere(V3(0, -0.25, -2), 0.05, buttons) )
    r.scene.append( Sphere(V3(0, -0.5, -2), 0.05, buttons) )

    # Smile
    r.scene.append( Sphere(V3(0.045, 0.25, -2), 0.02, smile) )
    r.scene.append( Sphere(V3(0.1, 0.30, -2), 0.02, smile) )
    r.scene.append( Sphere(V3(-0.045, 0.25, -2), 0.02, smile) )
    r.scene.append( Sphere(V3(-0.1, 0.30, -2), 0.02, smile) )

    # Nose
    r.scene.append( Sphere(V3(0, 0.32, -2), 0.02, carrot) )

    # Eyes
    r.scene.append( Sphere(V3(0.075, 0.4, -2), 0.04, eye) )
    r.scene.append( Sphere(V3(-0.075, 0.4, -2), 0.04, eye) )


    
    r.rtRender()

    r.glFinish('output.bmp')

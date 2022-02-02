import numpy as np
from scene import Scene
from manifolds import BezierCurve, Circle, ConcaveSegment, ConvexSegment, LinearSegment, Shape
from nanogui import nanovg as nvg
from bezier_shapes import *

def horse_shoe_scene():
	# horse shoe shape
    eta_epoxy = 1.49
    # eta_pdms = 1.421
    eta_pdms = 1.44
    # dim
    orad = 11.94/10
    thi = 4.7/10
    height = 7.95/10

    # start
    s0 = LinearSegment([-orad-thi*2, -0.1*10], [-orad+thi*10, -0.1*10])
    s0.type = Shape.Type.Diffuse
    s0.start = True

    # end
    se = LinearSegment([-orad+thi*6, 5], [-orad, 5])
    se.type = Shape.Type.Diffuse
    se.eta = eta_epoxy

    # scene lines
    s1 = LinearSegment([-orad+thi, 0], [-orad, 0])
    s1.type = Shape.Type.Refraction
    s1.eta = eta_epoxy
    s1.first_specular = True

    s2 = LinearSegment([-orad+thi, height], [-orad+thi, 0])
    s2.type = Shape.Type.Refraction
    s2.eta = eta_epoxy

    s3 = ConvexSegment([-orad+thi, height], [orad-thi, height], orad-thi, False)
    s3.type = Shape.Type.Refraction
    s3.eta = 1.0/eta_epoxy
    
    s4 = LinearSegment([orad-thi, 0], [orad-thi, height])
    s4.type = Shape.Type.Refraction
    s4.eta = eta_epoxy
    
    s5 = LinearSegment([orad, 0], [orad-thi, 0])
    s5.type = Shape.Type.Refraction
    s5.eta = eta_epoxy

    s6 = LinearSegment([-orad, 0], [-orad, height])
    s6.type = Shape.Type.Refraction
    s6.eta = eta_epoxy/eta_pdms

    # eta setting eta_medium_oppo_normal/eta_medium_with_normal

    s6_mirror = LinearSegment([orad, height], [orad, 0])
    s6_mirror.type = Shape.Type.Refraction
    s6_mirror.eta = eta_epoxy/eta_pdms

    s7 = ConvexSegment([-orad, height], [orad, height], orad, False)
    s7.type = Shape.Type.Refraction
    s7.eta = eta_epoxy/eta_pdms

    # diffuse arc
    s8 = ConcaveSegment([orad+thi-1e-5, height], [-(orad+thi-1e-5), height], orad+thi)
    s8.type = Shape.Type.Reflection
    s8.first_specular = True
    
    s9 = LinearSegment([-orad-thi, height], [-orad-thi, 0])
    s9.type = Shape.Type.Reflection

    s9_mirror = LinearSegment([orad+thi, 0], [orad+thi, height])
    s9_mirror.type = Shape.Type.Reflection

    s10 = LinearSegment([-(orad), 0], [-(orad+thi), 0])
    s10.type = Shape.Type.Refraction
    s10.eta = eta_pdms

    s10_mirror = LinearSegment([orad+thi, 0], [orad, 0])
    s10_mirror.type = Shape.Type.Refraction
    s10_mirror.eta = eta_pdms
    
    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s0,  se,
        s1, s3,s7,
        s2, s4, s5, 
        s6, s6_mirror,
        s8, 
        s9, s9_mirror,
        s10, s10_mirror,
         bounds])

    # scene = Scene([s0,  se,
    #     s8, 
    #      bounds])

    scene.name = "horse shoe"
    scene.set_start(0.55, 85, 1.0, 0.5)
    scene.offset = [0, -2]
    scene.zoom = 0.2
    # scenes.insert(0, scene)

    return scene
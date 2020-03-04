import numpy as np
from scene import Scene
from manifolds import BezierCurve, Circle, ConcaveSegment, ConvexSegment, LinearSegment, Shape
from nanogui import nanovg as nvg
from bezier_shapes import *

def create_scenes():
    scenes = []

    s1 = LinearSegment([-0.7, 0], [0.7, 0])
    s1.type = Shape.Type.Diffuse
    s1.end = True

    s2 = LinearSegment([0.7, 1.5], [-0.7, 1.5])
    s2.type = Shape.Type.Diffuse
    s2.start = True

    scale = 0.6
    offset = 0.2
    pool_x = pts_pool[0]
    pool_y = pts_pool[1]
    pool_x *= scale; pool_y *= scale
    pool_y += offset

    s3 = BezierCurve(list(pool_x.flatten()), list(pool_y.flatten()))
    s3.type = Shape.Type.Refraction
    s3.eta = 1.33
    s3.first_specular = True

    s4 = LinearSegment([-0.6, 0.5], [-0.55, 0.5])
    s4.type = Shape.Type.Diffuse
    s4.gradient_start = 9.31
    s4.gradient_width = 0.08
    s4.height = 10.0

    s5 = LinearSegment([0.55, 0.5], [0.6, 0.5])
    s5.type = Shape.Type.Diffuse
    s5.gradient_start = 9.31
    s5.gradient_width = 0.08
    s5.height = 10.0



    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s3, s1, s2, s4, s5, bounds])
    scene.name = "Pool"
    scene.set_start(0.1, -121.429, 0.3849, 0.5)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)






    s1 = LinearSegment([-0.7, 0], [0.7, 0])
    s1.type = Shape.Type.Diffuse
    # s1.end = True

    s2 = LinearSegment([0.7, 1.5], [-0.7, 1.5])
    s2.type = Shape.Type.Diffuse
    s2.start = True
    s2.end = True

    siggraph_1_x = pts_siggraph_1[0]
    siggraph_1_y = pts_siggraph_1[1]
    siggraph_2_x = pts_siggraph_2[0]
    siggraph_2_y = pts_siggraph_2[1]
    siggraph_3_x = pts_siggraph_3[0]
    siggraph_3_y = pts_siggraph_3[1]
    siggraph_4_x = pts_siggraph_4[0]
    siggraph_4_y = pts_siggraph_4[1]
    mitsuba_x = pts_mitsuba[0]
    mitsuba_y = pts_mitsuba[1]

    scale = 0.65
    offset = 0.7
    siggraph_1_x *= scale; siggraph_2_x *= scale; siggraph_3_x *= scale; siggraph_4_x *= scale;
    siggraph_1_y *= scale; siggraph_2_y *= scale; siggraph_3_y *= scale; siggraph_4_y *= scale;
    siggraph_1_y += offset; siggraph_2_y += offset; siggraph_3_y += offset; siggraph_4_y += offset;
    mitsuba_x *= scale; mitsuba_y *= scale
    mitsuba_y += offset

    s3 = BezierCurve(list(siggraph_1_x.flatten()), list(siggraph_1_y.flatten()))
    s3.type = Shape.Type.Refraction
    s3.eta = 1.5
    s3.first_specular = True

    s4 = BezierCurve(list(siggraph_2_x.flatten()), list(siggraph_2_y.flatten()))
    s4.type = Shape.Type.Refraction
    s4.eta = 1.5

    s5 = BezierCurve(list(siggraph_3_x.flatten()), list(siggraph_3_y.flatten()))
    s5.type = Shape.Type.Refraction
    s5.eta = 1.5

    s6 = BezierCurve(list(siggraph_4_x.flatten()), list(siggraph_4_y.flatten()))
    s6.type = Shape.Type.Refraction
    s6.eta = 1.5

    s7 = BezierCurve(list(mitsuba_x.flatten()), list(mitsuba_y.flatten()))
    s7.type = Shape.Type.Refraction
    s7.eta = 1.5

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s2, s3, s4, s5, bounds])
    scene.name = "Test"
    scene.set_start(0.1, -121.429, 0.3429, 0.5)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)



    s1 = LinearSegment([0.7, 1.5], [-0.7, 1.5])
    s1.type = Shape.Type.Diffuse
    s1.end = True
    s1.start = True

    s3 = ConvexSegment([-0.6, 0.5], [0.6, 0.5], 2.0, False)
    s3.type = Shape.Type.Reflection
    s3.first_specular = True


    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s3, bounds])
    scene.name = "Reflection"
    scene.set_start(0.1, -121.65789, 0.9, 0.5)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)



    s1 = LinearSegment([-0.7, 0], [0.7, 0])
    s1.type = Shape.Type.Diffuse
    s1.end = True

    s2 = LinearSegment([0.7, 1.5], [-0.7, 1.5])
    s2.type = Shape.Type.Diffuse
    s2.start = True

    s3 = ConvexSegment([-0.6, 0.5], [0.6, 0.5], 2.0, False)
    s3.type = Shape.Type.Refraction
    s3.eta = 1.5
    s3.first_specular = True
    s3.gradient_start = 0.4

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s2, s3, s1, bounds])
    scene.name = "Refraction"
    scene.set_start(0.1, -121.429, 0.3429, 0.5)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)



    s1 = LinearSegment([-0.8, 0], [0.8, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True
    s1.end = True

    s2 = Circle([0.0, 1.0], 0.5)
    s2.type = Shape.Type.Refraction
    s2.eta = 1.5
    s2.first_specular = True

    s3 = LinearSegment([0.8, 2], [-0.8, 2])
    s3.type = Shape.Type.Reflection

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s2, s3, bounds])
    scene.name = "Multiple bounces (Circle)"
    scene.set_start(0.41, 100.61)
    scene.offset = [0, -1]
    scene.zoom = 0.75
    scenes.append(scene)



    s1 = LinearSegment([-0.8, 0], [0.8, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True
    s1.end = True

    bunny_x = pts_bunny[0]; bunny_x *= 0.6
    bunny_y = pts_bunny[1]; bunny_y *= 0.6; bunny_y += 1.0
    s2 = BezierCurve(list(bunny_x.flatten()), list(bunny_y.flatten()))
    s2.type = Shape.Type.Refraction
    s2.eta = 1.5
    s2.first_specular = True

    s3 = LinearSegment([0.8, 2], [-0.8, 2])
    s3.type = Shape.Type.Reflection

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s2, s3, bounds])
    scene.name = "Multiple bounces (Bunny)"
    scene.set_start(0.6443710327148438, 85.17827)
    scene.offset = [0, -1]
    scene.zoom = 0.75
    scenes.append(scene)



    s1 = LinearSegment([-0.7, 0], [0.7, 0])
    s1.type = Shape.Type.Diffuse

    s2 = LinearSegment([0.7, 1.5], [-0.7, 1.5])
    s2.type = Shape.Type.Diffuse
    s2.start = True
    s2.end = True

    plane_x = pts_wavy_plane[0]
    plane_y = pts_wavy_plane[1]
    plane_x *= 0.7;
    plane_y *= 0.7;
    plane_y += 0.08;

    s3 = BezierCurve(list(plane_x.flatten()), list(plane_y.flatten()))
    s3.type = Shape.Type.Reflection
    s3.first_specular = True

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s2, s3, s1, bounds])
    scene.name = "Wavy plane"
    scene.set_start(0.157, -121.429, 0.832, 0.5)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)





    s1 = LinearSegment([-0.7, 0], [0.7, 0])
    s1.type = Shape.Type.Diffuse

    s2 = LinearSegment([0.7, 1.5], [-0.7, 1.5])
    s2.type = Shape.Type.Diffuse
    s2.start = True
    s2.end = True

    dragon_x = pts_dragon[0]
    dragon_y = pts_dragon[1]
    dragon_hole_x = pts_dragon_hole[0]
    dragon_hole_y = pts_dragon_hole[1]
    dragon_x *= 0.7; dragon_hole_x *= 0.7
    dragon_y *= 0.7; dragon_hole_y *= 0.7
    dragon_y += 0.48; dragon_hole_y += 0.48


    s3 = BezierCurve(list(dragon_x.flatten()), list(dragon_y.flatten()))
    s3.type = Shape.Type.Reflection
    s3.first_specular = True
    s3.name = "dragon"

    s_hole = BezierCurve(list(dragon_hole_x.flatten()), list(dragon_hole_y.flatten()))
    s_hole.type = Shape.Type.Reflection
    # s_hole.flip()
    s_hole.hole = True
    s_hole.parent = "dragon"

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s2, s3, s1, s_hole, bounds])
    scene.name = "Dragon"
    scene.set_start(0.157, -121.429, 0.832, 0.5)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)



    s1 = LinearSegment([-1, 0], [-0.1, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True

    s2 = LinearSegment([0.1, 0], [1, 0])
    s2.type = Shape.Type.Diffuse
    s2.end = True

    s3 = LinearSegment([0.45, 1], [-0.45, 1])
    s3.type = Shape.Type.Reflection
    s3.first_specular = True

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s2, s3, bounds])
    scene.name = "Line segment"
    scene.set_start(0.5, 60)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)



    s1 = LinearSegment([-1, 0], [-0.1, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True

    s2 = LinearSegment([0.1, 0], [1, 0])
    s2.type = Shape.Type.Diffuse
    s2.end = True

    s3 = ConvexSegment([0.45, 2], [-0.45, 2], 0.7, True)
    s3.type = Shape.Type.Reflection
    s3.first_specular = True

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s2, s3, bounds])
    scene.name = "Curved segment (alt)"
    scene.set_start(0.5, 53)
    scene.offset = [0.13, -0.8]
    scene.zoom = 0.75
    scenes.append(scene)



    s1 = LinearSegment([-1, 0], [-0.1, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True

    s2 = LinearSegment([0.1, 0], [1, 0])
    s2.type = Shape.Type.Diffuse
    s2.end = True

    s3 = ConcaveSegment([0.45, 1], [-0.45, 1], 2.0)
    s3.type = Shape.Type.Reflection
    s3.first_specular = True

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s2, s3, bounds])
    scene.name = "Concave segment"
    scene.set_start(0.5, 60)
    scene.offset = [0, -0.75]
    scene.zoom = 0.93
    scenes.append(scene)



    s1 = LinearSegment([-1.0, 0], [1.0, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True

    s2 = Circle([0.0, 0.0], 1.0)
    s2 = ConvexSegment([-0.9, 0], [0.9, 0], 0.9, True)
    s2.type = Shape.Type.Refraction
    s2.eta = 2.0
    s2.first_specular = True

    # s3 = LinearSegment([1.0, 2.0], [-1.0, 2.0])
    s3 = LinearSegment([1.15, 1.5], [0.95, 1.8])
    s3.type = Shape.Type.Diffuse
    s3.end = True
    s3.gradient_start = 0.08

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s2, s1, s3, bounds])
    scene.name = "MNEE"
    scene.set_start(0.3, 65.433, 0.5, 0.5)
    scene.offset = [0, -1]
    scene.zoom = 0.65
    scenes.append(scene)



    s1 = LinearSegment([-1.0, 0], [1.0, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True

    s2 = Circle([0.0, 0.0], 1.0)
    s2 = ConvexSegment([-0.9, 0], [0.9, 0], 0.9, True)
    s2.type = Shape.Type.Refraction
    s2.eta = 2.0
    s2.first_specular = True

    # s3 = LinearSegment([1.0, 2.0], [-1.0, 2.0])
    s3 = LinearSegment([1.35, 0.8], [1.3, 1.0])
    s3.type = Shape.Type.Diffuse
    s3.end = True
    s3.gradient_start = 0.08

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s2, s1, s3, bounds])
    scene.name = "MNEE (Constraints)"
    scene.set_start(0.3, 65.433, 0.5, 0.2632)
    scene.offset = [0, -1]
    scene.zoom = 0.65
    scenes.append(scene)



    s1 = LinearSegment([-0.5, 0], [0.5, 0])
    s1.type = Shape.Type.Diffuse
    s1.start = True

    s2 = Circle([0.0, 1.0], 0.3)
    s2.type = Shape.Type.Refraction
    s2.eta = 1.5
    s2.first_specular = True

    s3 = LinearSegment([0.5, 1.8], [-0.5, 1.8])
    s3.type = Shape.Type.Diffuse
    s3.end = True

    bounds = Circle([0, 0], 100.0)
    bounds.type = Shape.Type.Null
    bounds.visible = False

    scene = Scene([s1, s2, s3, bounds])
    scene.name = "Circle"
    scene.set_start(0.675, 87.7394, 0.7552, 0.5)
    scene.offset = [0, -1]
    scene.zoom = 0.75
    scene.n_bounces_default = 2
    scenes.append(scene)


    return scenes

#
# animation_glance.py
# animation data structure
#
import os
import bpy
os.system("cls")

# refer
o_arma = bpy.data.objects[0]
o_mesh = bpy.data.objects[2]
arma = o_arma.data
mesh = o_mesh.data
scene = bpy.data.scenes[0]
action = None

# armature and bone
print("------------------")
print("armature and bone:")
print("------------------")
ix = 1
print("bones:\t\t", arma.bones)
print("index:\t\t", ix)
print("bones[ix]:\t", arma.bones[ix])
print("children:\t", arma.bones[ix].children)
print("parent:\t\t", arma.bones[ix].parent)
print("matrix_local:") 
print(arma.bones[ix].matrix_local)

# maximum number of bones per vertex
print("")
print("-----------------------------------")
print("maximum number of bones per vertex:")
print("-----------------------------------")
count = 0
for v in mesh.vertices:
	if len(v.groups) > 4:
		count += 1
print("total of vertexes which has more than 4 bones:\t", count)

# action
print("")
print("-------")
print("action:")
print("-------")
try:
	action = bpy.data.actions[0]
	print("frame_rage:\t", action.frame_range)
except:
	print("action data is not prepared")

# scene and pose
print("")
print("---------------")
print("scene and pose:")
print("---------------")

scene.frame_set(10)
scene.update()
print("fps:\t\t", scene.render.fps)
print("frame_current:\t", scene.frame_current)
print("bones[ix]:\t", o_arma.pose.bones[ix])
print("matrix:")
print(o_arma.pose.bones[ix].matrix)

#
# animation_glance.py
# animation data structure
#
import os
import bpy
os.system("cls")

# find specific type index from objects
obj_ix_arma = -1
obj_ix_mesh = -1

# find_first_object
def find_first_object(str_type):
	for ix, obj in enumerate(bpy.data.objects):
		if obj.type == str_type:
			print("object["+str(ix)+"]\t", obj.type)
			return ix
	return -1

# armatures
print("----------")
print("armatures:")
print("----------")
print("armatures\t", bpy.data.armatures)
print("objects\t\t", bpy.data.objects)
obj_ix_arma = find_first_object("ARMATURE")
obj_ix_mesh = find_first_object("MESH")

# refer
o_arma = bpy.data.objects[obj_ix_arma]
o_mesh = bpy.data.objects[obj_ix_mesh]
arma = o_arma.data
mesh = o_mesh.data
scene = bpy.data.scenes[0]
action = None

# first armature and bone
ix_bone = 0
print("")
print("----------------------------")
print("first armature and bones["+str(ix_bone)+"]:")
print("----------------------------")
print("bones:\t\t", arma.bones)
print("bones["+str(ix_bone)+"]:\t", arma.bones[ix_bone])
print("parent:\t\t", arma.bones[ix_bone].parent)
print("matrix_local:")
print(arma.bones[ix_bone].matrix_local)

# maximum number of bones per vertex
print("")
print("-----------------------------------")
print("maximum number of bones per vertex:")
print("-----------------------------------")
count = 0
for v in mesh.vertices:
	if len(v.groups) > 4:
		count += 1
print("vertexes which has more than 4 bones:\t", count)

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

scene.frame_set(1)
scene.update()
print("fps:\t\t", scene.render.fps)
print("frame_current:\t", scene.frame_current)
print("bones["+str(ix_bone)+"]:\t", o_arma.pose.bones[ix_bone])
print("matrix:")
print(o_arma.pose.bones[ix_bone].matrix)

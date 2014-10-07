#
# animation_glance.py
# animation data structure
#
import os
import bpy
os.system("cls")

o_arma = bpy.data.objects[0]
o_mesh = bpy.data.objects[2]
arma = bpy.data.objects[0].data
mesh = bpy.data.objects[2].data
c_obj = bpy.context.object

# armature and bone
print("------------------")
print("armature and bone:")
print("------------------")
ix = 0
print("bones:\t\t", arma.bones)
print("index:\t\t", ix)
print("bones[ix]:\t", arma.bones[ix])
print("children:\t", arma.bones[ix].children)
print("parent:\t\t", arma.bones[ix].parent)
print("head:\t\t", arma.bones[ix].head)
print("tail:\t\t", arma.bones[ix].tail)
print("length:\t\t", arma.bones[ix].length)
print("matrix:")
print(arma.bones[ix].matrix)
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
	obj = bpy.data.actions[0]
	print("frame_rage:\t", obj.frame_range)
	print("groups:\t\t", obj.groups)
except:
	print("action data is not prepared")

# scene and pose
print("")
print("---------------")
print("scene and pose:")
print("---------------")
obj = bpy.data.scenes[0]
obj.frame_set(10)
obj.update()
print("frame_current:\t", obj.frame_current)
print("tail:\t\t", c_obj.pose.bones[ix].tail)
print("location:\t", c_obj.pose.bones[ix].location)
print("matrix:")
print(c_obj.pose.bones[ix].matrix)
print("scale:\t\t", c_obj.pose.bones[ix].scale)
print("rotation_quaternion:\t", c_obj.pose.bones[ix].rotation_quaternion)
print("tail:\t\t", c_obj.pose.bones[ix].bone.tail)
print("bones[ix]:\t", c_obj.pose.bones[ix])
print("matrix_basis:")
print(c_obj.pose.bones[ix].matrix_basis)

# object armature
print("")
print("----------------")
print("object armature:")
print("----------------")
print("matrix_basis")
print(o_arma.matrix_basis)
print("matrix_local")
print(o_arma.matrix_local)
print("matrix_parent_inverse")
print(o_arma.matrix_parent_inverse)
print("matrix_world")
print(o_arma.matrix_world)

#
print("")
print("-----")
print("test:")
print("-----")
import copy
import mathutils
bone_length = copy.deepcopy(arma.bones[ix].length)
bone_head = copy.deepcopy(arma.bones[ix].head)
bone_translation = mathutils.Matrix.Translation(mathutils.Vector((0, bone_length, 0)) + bone_head)
print(bone_translation)

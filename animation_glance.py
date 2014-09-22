#
# animation_glance.py
# Animation data structure
#
import os
import bpy
os.system("cls")

o_arma = bpy.data.objects[0]
o_mesh = bpy.data.objects[2]
arma = bpy.data.objects[0].data
mesh = bpy.data.objects[2].data
c_obj = bpy.context.object

print("-------------------------")
print("Animation data structure:")
print("-------------------------")

# armatures
ix = 0
print("bones:\t\t", arma.bones)
print("index:\t\t", ix)
print("bones[ix]:\t", arma.bones[ix])
print("children:\t", arma.bones[ix].children)
print("parent:\t\t", arma.bones[ix].parent)
print("tail:\t\t", arma.bones[ix].tail)
print("matrix:")
print(arma.bones[ix].matrix)
print("matrix_local:")
print(arma.bones[ix].matrix_local)

# maximum number of bones per vertex
count = 0
for v in mesh.vertices:
	if len(v.groups) > 4:
		count += 1
print("total of vertexes which has more than 4 bones:\t", count)

# action
obj = bpy.data.actions[0]
print("frame_rage:\t", obj.frame_range)
print("groups:\t\t", obj.groups)

# scene and pose
obj = bpy.data.scenes[0]
obj.frame_set(10)
print("frame_current:\t", obj.frame_current)
print("tail:\t\t", c_obj.pose.bones[ix].tail)
print("location:\t", c_obj.pose.bones[ix].location)
print("matrix:")
print(c_obj.pose.bones[ix].matrix)
print("scale:\t\t", c_obj.pose.bones[ix].scale)
print("rotation_quaternion:\t", c_obj.pose.bones[ix].rotation_quaternion)
print("tail:\t\t", c_obj.pose.bones[ix].bone.tail)
print("bones[ix]:\t", c_obj.pose.bones[ix])

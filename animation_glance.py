#
# animation_glance.py
# Animation data structure
#
import os
import bpy
os.system("cls")

arma = bpy.data.armatures[0]
obj = bpy.data.objects[2]
mesh = bpy.data.meshes[0]

print("-------------------------")
print("Animation data structure:")
print("-------------------------")

# armatures
index = 0
print("bones:\t\t", arma.bones)
print("index:\t\t", index)
print("bones[index]:\t", arma.bones[index])
print("children:\t", arma.bones[index].children)
print("parent:\t\t", arma.bones[index].parent)
print("head:\t\t", arma.bones[index].head)
print("head_local:\t", arma.bones[index].head_local)
print("tail:\t\t", arma.bones[index].tail)
print("tail_local:\t", arma.bones[index].tail_local)
print("matrix:")
print(arma.bones[index].matrix)
print("matrix_local:")
print(arma.bones[index].matrix_local)
#
count = 0
for v in mesh.vertices:
	if len(v.groups) > 4:
		count += 1
print("vertex over:\t", count)
print("vertex_groups:\t",obj.vertex_groups)

#
# animation_export.py
# export animation data to text
#
import os
import copy
import bpy
import mathutils
os.system("cls")

# refer
o_arma = bpy.data.objects[0]
o_mesh = bpy.data.objects[2]
arma = o_arma.data

# ini var
mat_to_root = []
mat_offset = []

# get index
def get_index(item, bpy_data):
	for index, item_e in enumerate(bpy_data):
		if item_e == item:
			return index
	return -1

# bone hierarchy
print("bone hierarchy:")
for index, item in enumerate(arma.bones):
	print(index, get_index(item.parent, arma.bones))

# offset transformation, mesh to armature
def get_offset(ix):
	return arma.bones[ix].matrix_local

# get postion, quat, scale 
def get_mat_deco(ix):
	return o_arma.pose.bones[ix].matrix.decompose()

# test
print("test")
print(get_offset(3))
loc, rot, sca = get_mat_deco(3)
print(loc)
print(rot)
print(sca)

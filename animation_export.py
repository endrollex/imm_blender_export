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
data_offset = []
data_hierarchy = []

# get index
def get_index(item, bpy_data):
	for index, item_e in enumerate(bpy_data):
		if item_e == item:
			return index
	return -1

# get bone hierarchy
def data_hierarchy():
	rt_list = []
	for index, item in enumerate(arma.bones):
		rt_list.append([index, get_index(item.parent, arma.bones)])
	return rt_list

# offset transformation, mesh to armature
def data_offset(ix):
	return mathutils.Matrix.transposed(arma.bones[ix].matrix_local)

# get postion, quat, scale
def get_mat_deco(ix):
	return o_arma.pose.bones[ix].matrix.decompose()

# set frame
def set_frame(frame):
	scene.frame_set(frame)
	scene.update()

# test
print("test")
print(data_offset(3))
loc, rot, sca = get_mat_deco(3)
print(loc)
print(rot)
print(sca)
print(data_hierarchy())

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
arma = bpy.data.armatures[0]
o_arma = bpy.data.objects[0]
o_mesh = bpy.data.objects[2]

# ini var
mat_to_root = []

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

# to parent
def to_parent(ix):
	# if have not parent, return to_root
	# assume there is only one root bone
	if arma.bones[ix].parent == None:
		return o_arma.matrix_basis
	return mathutils.Matrix.Translation(arma.bones[ix].parent.tail_local - arma.bones[ix].parent.head_local)

# to root i
def to_root_i(ix):
	if arma.bones[ix].parent != None:
		mat_to_root[ix] = to_parent(ix)*mat_to_root[get_index(arma.bones[ix].parent, arma.bones)]

# calc to root i
for ixl in range(0, len(arma.bones)):
	mat_to_root.append(None)
mat_to_root[0] = to_parent(0)
for ixl in range(0, len(arma.bones)):
	to_root_i(ixl)
for ixl in range(0, len(mat_to_root)):
	print("bone", ixl)
	print(mat_to_root[ixl])

# offset, mesh to armature
offset = mathutils.Matrix.Identity(4)

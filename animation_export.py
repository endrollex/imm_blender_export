#
# animation_export.py
# export animation data to text
#
import os
import copy
import bpy
os.system("cls")
arma = bpy.data.armatures[0]

# get index
def get_index(item, bpy_data):
	for index, item_e in enumerate(bpy_data):
		if item_e == item:
			return index
	return -1

# BoneHierarchy
for index, item in enumerate(arma.bones):
	print(index, get_index(item.parent, arma.bones))

# BoneOffsets

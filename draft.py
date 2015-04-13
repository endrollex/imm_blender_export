#
# draft.py
# draft
#
# ignore this file
#
import os
import bpy
import mathutils
import datetime
import sys
sys.path.append("C:\\Dropbox\\imm_blender_export\\")
import export_static
import global_var
os.system("cls")

# armature
objects_arma = export_static.find_first_object("ARMATURE")
o_arma = bpy.data.objects[objects_arma[0]]
arma = o_arma.data

# mesh
objects_mesh = export_static.find_mesh()
o_mesh = bpy.data.objects[objects_mesh[0]]
mesh = o_mesh.data

'''
# print rigify
rig_list = []
for index, bone in enumerate(arma.bones):
	None
	#if bone.name.find("ORG") != -1:
	#print(index, bone.name)
	temp = str(index) + " " + bone.name
	rig_list.append(temp)
print(len(arma.bones))
print(arma.bones[0].name)
export = global_var.export_dir+"rig.txt"
#export_static.write_text(export, rig_list)
'''

'''
# pirnt vertex gruop
print(mesh.vertices[0].groups[0].group)
print(o_mesh.vertex_groups)
for index, gro in enumerate(o_mesh.vertex_groups):
	None
	#print(index, gro.name)
'''

# read bone hierarchy text
rigify_list = []
rigify_dict = {}
rigify_dict_inv = {}
#
read_path = global_var.export_dir+"rigify_ORG.csv"
f = open(read_path)
rigify_list = f.read().splitlines()
f.close()
for line in rigify_list:
	None
	#print(line)
#
print(len(rigify_list))
print(rigify_list.index("ORG-toe.R"))
#
for index, bone in enumerate(arma.bones):
	if bone.name in rigify_list:
		rigify_dict[bone.name] = index
		rigify_dict_inv[index] = bone.name
for (k, v) in rigify_dict.items():
    print(v, k)
print(len(rigify_dict))
print(len(rigify_dict_inv))


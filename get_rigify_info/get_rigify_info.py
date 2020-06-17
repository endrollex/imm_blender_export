#
# get_rigify_info.py
#
import os
import bpy
import mathutils
import datetime
import sys
WORKING_DIR = "D:\\\EndrDocument\\ModelAnim\\imm_blender_export\\"
EXPORT_DIR = WORKING_DIR
sys.path.append(WORKING_DIR)
import imm_static
imm_static.set_global_dict("IS_RIGIFY", True)
os.system("cls")

# armature
objects_arma = imm_static.find_first_object("ARMATURE")
o_arma = bpy.data.objects[objects_arma[0]]
arma = o_arma.data

# mesh
objects_mesh = imm_static.find_mesh()
o_mesh = bpy.data.objects[objects_mesh[0]]
mesh = o_mesh.data

# print arma
def print_arma():
	for index, bone in enumerate(arma.bones):
		print(bone.name)

# get rig list
def get_rig_list():
	rig_list = []
	for index, bone in enumerate(arma.bones):
		if bone.name.find("ORG") != -1:
			#print(index, bone.name)
			temp = str(index) + "," + bone.name
			rig_list.append(temp)
	#
	export = EXPORT_DIR+"get_rig_list.txt"
	imm_static.write_text(export, rig_list)

# get vertex group
def get_vertex_group():
	#print(mesh.vertices[0].groups[0].group)
	#print(o_mesh.vertex_groups)
	group_list = []
	for index, gro in enumerate(o_mesh.vertex_groups):
		#print(index, gro.name)
		temp = str(index) + "," + gro.name
		group_list.append(temp)
	export = EXPORT_DIR+"get_vertex_group.txt"
	imm_static.write_text(export, group_list)


# read bone hierarchy text
rigify_list = []
rigify_dict = {}
rigify_dict_inv = {}
#
def print_hierarchy():
	print("print_hierarchy")
	print("-------------------------------------------------------")
	read_path = WORKING_DIR+"rigify_custom\\default_hierarchy.csv"
	f = open(read_path)
	rigify_list = f.read().splitlines()
	f.close()
	for line in rigify_list:
		None
		#print(line)
	#
	for index, bone in enumerate(arma.bones):
		if bone.name in rigify_list:
			rigify_dict[bone.name] = index
			rigify_dict_inv[index] = bone.name
	for (k, v) in rigify_dict.items():
		print(v, k)
	print(len(rigify_list))
	print(rigify_list.index("ORG-toe.R"))
	print(len(rigify_dict))
	print(len(rigify_dict_inv))

# read group map
def print_group_map():
	print("print_group_map")
	print("-------------------------------------------------------")
	rigify_group = []
	read_path = WORKING_DIR+"rigify_custom\\default_map.csv"
	f = open(read_path)
	temp = f.read().splitlines()
	f.close()
	for line in temp:
		rigify_group.append(line.split(","))
	for gro_map in rigify_group:
		print(gro_map[0], gro_map[1])

#
#get_rig_list()
#get_vertex_group()
#print_hierarchy()
#print_group_map()
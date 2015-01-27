#
# lib_export.py
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#
import os
import bpy
import math
import mathutils
import sys
sys.path.append("D:\\Dropbox\\imm_blender_export\\")
import global_var
os.system("cls")

# calc_tess
def calc_tess(mesh):
	if len(mesh.tessfaces) == 0:
		mesh.calc_tessface()

# find_mesh, mesh which must has uv
def find_mesh():
	obj_list = []
	for ix, obj in enumerate(bpy.data.objects):
		if obj.type == "MESH":
			mesh = mesh = bpy.data.objects[ix].data
			calc_tess(mesh)
			if len(mesh.uv_textures) > 0:
				obj_list.append(ix)
	return obj_list

# find_arma
def find_arma():
	for ix, obj in enumerate(bpy.data.objects):
		if obj.type == "ARMATURE":
			return [ix]
	return []

# if left hand, flip uv along X
def uv_flip_x(vec2_in):
	if global_var.is_left_hand:
		return mathutils.Vector((vec2_in.x, 1-vec2_in.y))
	return mathutils.Vector((vec2_in.x, vec2_in.y))

# get uv list and tessface list
# Blender's uv is per tessface
# we need uv per vertex
def data_uv_and_face(mesh):
	# store vertex of tessface
	tessface_list = []
	# check tessfaces, to avoid repeated calc_tessface
	calc_tess(mesh)
	# deepcopy manually
	for t in mesh.tessfaces:
		if len(t.vertices) == 4:
			tessface_list.append([t.vertices[0], t.vertices[1], t.vertices[2], t.vertices[3]])
		else:
			tessface_list.append([t.vertices[0], t.vertices[1], t.vertices[2]])
	# store uv according to vertex of tessface
	uv_data = mesh.tessface_uv_textures[0].data
	uv_list = []
	uv_ex_dict = {}
	uv_ex_dict_inv = {}
	vertex_count = len(mesh.vertices)
	for ix in range(0, vertex_count):
		uv_list.append([])
	uv_temp = [None, None, None, None]
	for ix in range(0, len(uv_data)):
		v = len(uv_data[ix].uv)
		uv_temp[0] = uv_flip_x(uv_data[ix].uv1)
		uv_temp[1] = uv_flip_x(uv_data[ix].uv2)
		uv_temp[2] = uv_flip_x(uv_data[ix].uv3)
		if v == 4:
			uv_temp[3] = uv_flip_x(uv_data[ix].uv4)
		for iv in range(0, v):
			if uv_temp[iv] not in uv_list[tessface_list[ix][iv]]:
				uv_list[tessface_list[ix][iv]].append(uv_temp[iv])
				len_uv_this = len(uv_list[tessface_list[ix][iv]])
				#
				uv_last_one = -1
				if len_uv_this > 1:
					uv_list.append([uv_temp[iv]])
					uv_last_one = len(uv_list)-1
				if len_uv_this == 2:
					# inial uv_ex_dict_inv
					# uv_ex_dict_inv: {vertex index: [exceed uv of this vertex]}
					uv_ex_dict_inv.fromkeys([tessface_list[ix][iv]])
					uv_ex_dict_inv[tessface_list[ix][iv]] = [uv_last_one]
				if len_uv_this > 2:
					uv_ex_dict_inv[tessface_list[ix][iv]].append(uv_last_one)
				if len_uv_this > 1:
					# uv_ex_dict: {uv index which exceed vertex count: vertex index}
					uv_ex_dict.fromkeys([uv_last_one])
					uv_ex_dict[uv_last_one] = tessface_list[ix][iv]
					tessface_list[ix][iv] = uv_last_one
				#
			else:
				if uv_temp[iv] != uv_list[tessface_list[ix][iv]][0]:
					for ix_uv in range(1, len(uv_list[tessface_list[ix][iv]])):
						if uv_temp[iv] == uv_list[tessface_list[ix][iv]][ix_uv]:
							tessface_list[ix][iv] = uv_ex_dict_inv[tessface_list[ix][iv]][ix_uv-1]
							break
	# rebuild uv list
	temp = uv_list
	uv_list = []
	for t in temp:
		uv_list.append(t[0])
	return [uv_list, uv_ex_dict, tessface_list]

#
objects_mesh = find_mesh()
objects_arma = find_arma()

mesh = bpy.data.objects[objects_mesh[0]].data
d_uv, d_uv_ex_dict, d_tessface = data_uv_and_face(mesh)
print(len(d_uv), len(d_uv_ex_dict), len(d_tessface))

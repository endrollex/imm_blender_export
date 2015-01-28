#
# lib_export_anim.py
# export animation data to text
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#
import os
import bpy
import mathutils
import datetime
import sys
sys.path.append("D:\\Dropbox\\imm_blender_export\\")
import static_export
import global_var
os.system("cls")

# global var
fcurve_keys_max = 0

####################################################################################################
# format functions
####################################################################################################
####################################################################################################

# matrix right to left hand
def to_left_matrix(mat):
	if not global_var.is_left_hand:
		return mat
	s_x = mathutils.Matrix.Identity(3)
	s_x[0][0] = -1
	mat_l = mat.to_3x3()
	mat_l = s_x*mat_l*s_x
	mat_l = mat_l.to_4x4()
	mat_l[3][0:3] = -mat[3][0], mat[3][1], mat[3][2]
	return mat_l

# get index
def get_index(item, bpy_data):
	for index, item_e in enumerate(bpy_data):
		if item_e == item:
			return index
	return -1

# format matrix
def format_matrix(list_in):
	rt_list = []
	for mat in list_in:
		vec_list = static_export.format_vector(mat)
		temp = vec_list[0]
		for ix in range(1, len(vec_list)):
			temp += " "+vec_list[ix]
		rt_list.append(temp)
	return rt_list

# index to str
def index_to_str(list_in):
	str_out = str(list_in[0])
	for ix in range(1, len(list_in)):
		str_out = str_out+" "+str(list_in[ix])
	return str_out

# format index
def format_index(list_in):
	rt_list = []
	for l in list_in:
		rt_list.append(index_to_str(l))
	return rt_list

# number to string
def number_to_str(list_in):
	rt_list = []
	for num in list_in:
		rt_list.append(str(static_export.round_sig(num)))
	return rt_list

# get to parent matrix
def get_to_parent(ix):
	# test
	if o_arma.pose.bones[ix].parent == None:
		return o_arma.pose.bones[ix].matrix
	to_parent = o_arma.pose.bones[ix].parent.matrix.inverted()*o_arma.pose.bones[ix].matrix
	return to_parent

# data bone hierarchy
def data_hierarchy():
	rt_list = []
	for index, item in enumerate(arma.bones):
		rt_list.append([index, get_index(item.parent, arma.bones)])
	return rt_list

# data offset transformation, mesh to armature
def data_offset():
	mesh_to_arma = o_mesh.matrix_basis*o_arma.matrix_basis
	rt_list = []
	for ix in range(0, len(arma.bones)):
		mat = (mesh_to_arma*arma.bones[ix].matrix_local).transposed()
		mat = to_left_matrix(mat)
		mat = mat.inverted()
		rt_list.append(mat)
	return rt_list

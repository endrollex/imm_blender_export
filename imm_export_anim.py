#
# imm_export_anim.py
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
import imm_export
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

# format matrix
def format_matrix(list_in):
	rt_list = []
	for mat in list_in:
		vec_list = imm_export.format_vector(mat)
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
		rt_list.append(str(imm_export.round_sig(num)))
	return rt_list

####################################################################################################
# armature functions
####################################################################################################
####################################################################################################

# get index
def get_index(item, bpy_data):
	for index, item_e in enumerate(bpy_data):
		if item_e == item:
			return index
	return -1

# get to parent matrix
def get_to_parent(o_arma, ix):
	# test
	if o_arma.pose.bones[ix].parent == None:
		return o_arma.pose.bones[ix].matrix
	to_parent = o_arma.pose.bones[ix].parent.matrix.inverted()*o_arma.pose.bones[ix].matrix
	return to_parent

# data bone hierarchy
def data_hierarchy(arma):
	rt_list = []
	for index, item in enumerate(arma.bones):
		rt_list.append([index, get_index(item.parent, arma.bones)])
	return rt_list

# data offset transformation, mesh to armature
def data_offset(o_mesh, o_arma, arma):
	mesh_to_arma = o_mesh.matrix_basis*o_arma.matrix_basis
	rt_list = []
	for ix in range(0, len(arma.bones)):
		mat = (mesh_to_arma*arma.bones[ix].matrix_local).transposed()
		mat = to_left_matrix(mat)
		mat = mat.inverted()
		rt_list.append(mat)
	return rt_list

# data anim clip, time position scale rotation
def data_anim_clip(scene, action, o_arma):
	time_list = []
	pos_list = []
	sca_list = []
	rot_list = []
	# find completed framekeys in fcurves
	global fcurve_keys_max
	fcurve_keys_max = 0
	fcurve_ix = 0
	for ix_fcu in range(0, len(action.fcurves)):
		len_fcurve_keys = len(action.fcurves[ix_fcu].keyframe_points)
		if len_fcurve_keys > fcurve_keys_max:
			fcurve_keys_max = len_fcurve_keys
			fcurve_ix = ix_fcu
	# fps -> second
	frame_time = 1/scene.render.fps
	cnt_bone = 0
	# time
	for bone in o_arma.pose.bones:
		for key in action.fcurves[fcurve_ix].keyframe_points:
			time_list.append(key.co[0]*frame_time)
			pos_list.append(None)
			sca_list.append(None)
			rot_list.append(None)
		cnt_bone += 1
	# position scale rotation
	for ix_key, key in enumerate(action.fcurves[fcurve_ix].keyframe_points):
		len_key = len(action.fcurves[fcurve_ix].keyframe_points)
		scene.frame_set(key.co[0])
		scene.update
		for ix in range(0, cnt_bone):
			mat_to_p = get_to_parent(o_arma, ix).transposed()
			mat_to_p = to_left_matrix(mat_to_p)
			mat_to_p = mat_to_p.transposed()
			loc, rot, sca = mat_to_p.decompose()
			rot = mathutils.Quaternion((rot.x, rot.y, rot.z, rot.w))
			pos_list[ix*len_key+ix_key] = loc
			sca_list[ix*len_key+ix_key] = sca
			rot_list[ix*len_key+ix_key] = rot
	return [time_list, pos_list, sca_list, rot_list]

# reassign weight and index
def reassign_weight(vert_group_in):
	re_list = []
	for group in vert_group_in:
		re_list.append([group.group, group.weight])
	re_list = sorted(re_list, key=lambda student: student[1], reverse=True)
	len_list = len(re_list)
	if len_list > 4:
		re_list = re_list[0:4]
	sum_weight = 0.0
	for re in re_list:
		sum_weight += re[1]
	sum_weight_diff = 1.0-sum_weight
	if sum_weight_diff > 0.02:
		for re in re_list:
			re[1] += (re[1]/sum_weight)*sum_weight_diff
	if len_list < 4:
		for ix in range(0, 4-len_list):
			re_list.append([0, 0.0])
	return re_list

# data blender indices and weights
def data_b_index_weight(mesh):
	b_index = []
	b_weight = []
	for vert in mesh.vertices:
		b_index.append([])
		b_weight.append([])
		# only use 4 bone per vertex
		re_group = reassign_weight(vert.groups)
		for group in re_group:
			b_index[-1].append(group[0])
			b_weight[-1].append(group[1])
	return [b_index, b_weight]

# data blender indices and weights add according uv
def data_b_index_weight_add(len_uv, uv_ex_dict, d_b_index_weight):
	for ix in range(len_uv-len(uv_ex_dict), len_uv):
		d_b_index_weight[0].append(d_b_index_weight[0][uv_ex_dict[ix]])
		d_b_index_weight[1].append(d_b_index_weight[1][uv_ex_dict[ix]])
	return d_b_index_weight

####################################################################################################
# export functions
####################################################################################################
####################################################################################################

# package hierarchy
def package_hierarchy(list_in):
	rt_list = []
	for index in list_in:
		rt_list.append("P"+str(index[0])+": "+str(index[1]))
	return rt_list

# package offset
def package_offset(list_in):
	rt_list = []
	for ix in range(0, len(list_in)):
		rt_list.append("B"+str(ix)+": "+list_in[ix])
	return rt_list

# package time position scale rotation
def package_anim_clip(txt_time, txt_pos, txt_sca, txt_rot):
	rt_list = []
	global fcurve_keys_max
	if fcurve_keys_max == 0:
		print("imm export error: keyframes no date")
	for ix in range(0, len(txt_time)):
		if ix%fcurve_keys_max == 0:
			rt_list.append("B"+str(int(ix/fcurve_keys_max))+" #K: "+str(fcurve_keys_max)+" {")
		rt_list.append("T: "+txt_time[ix]+" P: "+txt_pos[ix]+" S: "+txt_sca[ix]+" Q: "+txt_rot[ix])
		if (ix-fcurve_keys_max+1)%fcurve_keys_max == 0:
			rt_list.append("}")
	return rt_list

# package vertex with animation data
def package_vertex_anim(len_uv, txt_position, txt_normal, txt_tangent, txt_uv, txt_b_index, txt_b_weight):
	rt_list = []
	for ix in range(0, len_uv):
		temp = "P: "+txt_position[ix]+"\n"
		temp += "T: "+txt_tangent[ix][0:-2]+"\n"
		temp += "N: "+txt_normal[ix]+"\n"
		temp += "T: "+txt_uv[ix]+"\n"
		temp += "W: "+txt_b_weight[ix]+"\n"
		temp += "I: "+txt_b_index[ix]+"\n"
		rt_list.append(temp)
	return rt_list

# package mesh anim
def package_mesh_anim(scene, objects_mesh, o_arma, arma, coll_action):
	# bone offset, all meshes need to has same matrix_basis
	o_mesh = bpy.data.objects[objects_mesh[0]]
	offset = data_offset(o_mesh, o_arma, arma)
	#
	hierarchy = data_hierarchy(arma)
	txt_offset = package_offset(format_matrix(offset))
	txt_hierarchy = package_hierarchy(hierarchy)
	txt_coll_anim_clip = []
	len_anim_clip = 0
	# action
	for action in coll_action:
		anim_clip = data_anim_clip(scene, action, o_arma)
		txt_time = number_to_str(anim_clip[0])
		txt_pos = imm_export.format_vector(anim_clip[1])
		txt_sca = imm_export.format_vector(anim_clip[2])
		txt_rot = imm_export.format_vector(anim_clip[3])
		txt_anim_clip = package_anim_clip(txt_time, txt_pos, txt_sca, txt_rot)	
		txt_coll_anim_clip.append("AnimationClip "+action.name)
		txt_coll_anim_clip.append("{")
		txt_coll_anim_clip += txt_anim_clip
		txt_coll_anim_clip.append("}")
		len_anim_clip += 1
	
		
		
	

# package bone offset hierarchy animation clips
def package_bone_anim(offset, hierarchy, anim_clip):
	txt_anim = [""]
	txt_anim.append("--------------------------------BoneOffsets-")
	txt_anim += offset
	txt_anim.append("")
	txt_anim.append("------------------------------BoneHierarchy-")
	txt_anim += hierarchy
	txt_anim.append("")
	txt_anim.append("-----------------------------AnimationClips-")
	txt_anim.append("AnimationClip Take1")
	txt_anim.append("{")
	txt_anim += anim_clip
	txt_anim.append("}")
	return txt_anim

# export m3d anim
def export_m3d_anim():
	time_start = datetime.datetime.now()
	#
	objects_arma = imm_export.find_first_object("ARMATURE")
	objects_mesh = imm_export.find_mesh()
	o_arma = bpy.data.objects[objects_arma[0]]
	arma = o_arma.data
	scene = bpy.data.scenes[0]
	coll_action = bpy.data.actions
	#
	package_mesh_anim(scene, objects_mesh, o_arma, arma, coll_action)
	
	
	
	#
	time_spend = datetime.datetime.now()-time_start
	# print
	print("-----------------------")
	print("M3D Export (Animation):")
	print("-----------------------")
	print("left hand:\t"+str(global_var.is_left_hand))
	print("export dir:\t"+global_var.export_dir)
	print("spend time:\t"+str(time_spend.total_seconds())+" seconds")

# export
export_m3d_anim()

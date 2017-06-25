#
# imm_anim.py
# export animation data to text
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#
import os
import bpy
import mathutils
import datetime
import imm_static

# global var
anim_fcurve_keys_max = 0
anim_len_bones = 0
anim_arma_list = []

# rigify
rig_arma_list = []
rig_arma_find_old_ix = {}
rig_old_ix_redirect = {}
rig_group_map = {}

####################################################################################################
# format functions
####################################################################################################
####################################################################################################

# matrix right to left hand
def to_left_matrix(mat):
	if not imm_static.getglobald("IS_LEFT_HAND"):
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
		vec_list = imm_static.format_vector(mat)
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
		rt_list.append(str(imm_static.round_sig(num)))
	return rt_list

####################################################################################################
# rigify functions
####################################################################################################
####################################################################################################

# check is rigify
def is_rigify(arma):
	is_rig = False
	for bone in arma.bones:
		if bone.name == "MCH-neck.follow":
			is_rig = True
			break
	if (len(arma.bones) < 400):
		is_rig = False
	return is_rig

# read hierarchy form text
def read_hierarchy_rigify(arma):
	# build rigify infomation
	global rig_arma_list
	global rig_arma_find_old_ix
	global rig_old_ix_redirect
	global rig_group_map
	global anim_len_bones
	# hierarchy
	read_path = imm_static.getglobald("WORKING_DIR")+imm_static.getglobald("RIGIFY_HIERARCHY")
	f = open(read_path)
	rig_arma_list = f.read().splitlines()
	f.close()
	for index, bone in enumerate(arma.bones):
		if bone.name in rig_arma_list:
			rig_arma_find_old_ix[bone.name] = index
			rig_old_ix_redirect[index] = rig_arma_list.index(bone.name)
	#
	anim_len_bones = len(rig_arma_list)
	# group
	read_path = imm_static.getglobald("WORKING_DIR")+imm_static.getglobald("RIGIFY_GROUP_MAP")
	f = open(read_path)
	temp = f.read().splitlines()
	f.close()
	temp_group = []
	for line in temp:
		temp_group = line.split(",")
		rig_group_map[temp_group[0]] = rig_arma_list.index(temp_group[1])
	#check
	check = False
	if len(rig_arma_list) == len(rig_arma_find_old_ix):
		check = True
	if not check:
		print("--ATTENTION!--")
		print("imm export error: rigify hierarchy read error")
		assert(False)
	return check

# data bone hierarchy
def data_hierarchy_rigify(arma):
	global rig_arma_list
	global rig_arma_find_old_ix
	global rig_old_ix_redirect
	rt_list = []
	for index, org_bone in enumerate(rig_arma_list):
		index_parent = get_index(arma.bones[rig_arma_find_old_ix[org_bone]].parent, arma.bones)
		# check
		if index_parent in rig_old_ix_redirect or index_parent == -1:
			if index_parent != -1:
				index_parent = rig_old_ix_redirect[index_parent]
		else:
			print("--ATTENTION!--")
			print("imm export error: hierarchy wrong")
			assert(False)
		if index_parent >= index:
			print("--ATTENTION!--")
			print("imm export error: hierarchy wrong, child's index bigger than parent's")
			assert(False)
		rt_list.append([index, index_parent])
	return rt_list

# data offset transformation, mesh to armature
def data_offset_rigify(o_mesh, o_arma, arma):
	global rig_arma_list
	global rig_arma_find_old_ix
	mesh_to_arma = o_mesh.matrix_basis*o_arma.matrix_basis
	rt_list = []
	for org_bone in rig_arma_list:
		mat = (mesh_to_arma*arma.bones[rig_arma_find_old_ix[org_bone]].matrix_local).transposed()
		mat = to_left_matrix(mat)
		mat = mat.inverted()
		rt_list.append(mat)
	return rt_list

# data anim clip, time position scale rotation
def data_anim_clip_rigify(scene, action, o_arma):
	global rig_arma_list
	global rig_arma_find_old_ix
	# set active action
	o_arma.animation_data.action = action
	time_list = []
	pos_list = []
	sca_list = []
	rot_list = []
	# find completed framekeys in fcurves
	global anim_fcurve_keys_max
	anim_fcurve_keys_max = 0
	key_co_set = set()
	for ix_fcu in range(0, len(action.fcurves)):
		for key in action.fcurves[ix_fcu].keyframe_points:
			key_co_set.add(key.co[0])
	key_co_list = sorted(key_co_set)
	anim_fcurve_keys_max = len(key_co_list);
	# fps -> second
	frame_time = 1/scene.render.fps
	# time
	for nothing in rig_arma_list:
		for key_co in key_co_list:
			time_list.append(key_co*frame_time)
			pos_list.append(None)
			sca_list.append(None)
			rot_list.append(None)
	# position scale rotation
	len_key = len(key_co_list)
	for ix_key, key_co in enumerate(key_co_list):
		scene.frame_set(key_co)
		scene.update
		for index, org_bone in enumerate(rig_arma_list):
			ix = index
			mat_to_p = get_to_parent(o_arma.pose.bones.get(org_bone)).transposed()
			mat_to_p = to_left_matrix(mat_to_p)
			mat_to_p = mat_to_p.transposed()
			loc, rot, sca = mat_to_p.decompose()
			rot = mathutils.Quaternion((rot.x, rot.y, rot.z, rot.w))
			pos_list[ix*len_key+ix_key] = loc
			sca_list[ix*len_key+ix_key] = sca
			rot_list[ix*len_key+ix_key] = rot
	return [time_list, pos_list, sca_list, rot_list]

# reassign weight and index
def reassign_weight_rigify(vert_group, redirect_group):
	re_list = []
	for group in vert_group:
		get_ix = -1
		for ix, re in enumerate(re_list):
			if re[0] == redirect_group[group.group]:
				if group.weight > re[1]:
					get_ix = ix
		if get_ix == -1:
			re_list.append([redirect_group[group.group], group.weight])
		else:
			# if same bone, re-calclate weight
			re_list[get_ix][1] = group.weight
	#
	re_list = sorted(re_list, key=lambda student: student[1], reverse=True)
	len_list = len(re_list)
	if len_list > 4:
		re_list = re_list[0:4]
	sum_weight = 0.0
	for re in re_list:
		sum_weight += re[1]
	sum_weight_diff = 1.0-sum_weight
	# sum_weight should be 1.0, or 0.0 for none influence
	# normalize
	if sum_weight_diff > 0.01 or sum_weight_diff < 0.01:
		for re in re_list:
			re[1] += (re[1]/sum_weight)*sum_weight_diff
	if len_list < 4:
		for ix in range(0, 4-len_list):
			re_list.append([0, 0.0])
	#
	return re_list

# data blender indices and weights
def data_ble_index_weight_rigify(mesh, o_mesh):
	global rig_group_map
	# get current group index map to target rigify
	redirect_group = {}
	for index, gro in enumerate(o_mesh.vertex_groups):
		redirect_group[index] = rig_group_map[gro.name]
	#
	ble_index = []
	ble_weight = []
	for vert in mesh.vertices:
		ble_index.append([])
		ble_weight.append([])
		# only use 4 bone per vertex
		re_group = reassign_weight_rigify(vert.groups, redirect_group)
		for group in re_group:
			ble_index[-1].append(group[0])
			ble_weight[-1].append(group[1])
	return [ble_index, ble_weight]
#

####################################################################################################
# armature functions
####################################################################################################
####################################################################################################

# build armature info
def build_arma_info(o_arma, arma):
	global anim_len_bones
	global anim_arma_list
	anim_len_bones = len(arma.bones)
	for bone in arma.bones:
		anim_arma_list.append(bone.name)

# get index
def get_index(item, bpy_data):
	for index, item_e in enumerate(bpy_data):
		if item_e == item:
			return index
	return -1

# get to parent matrix
def get_to_parent(pose_bone):
	if pose_bone.parent == None:
		return pose_bone.matrix
	to_parent = pose_bone.parent.matrix.inverted()*pose_bone.matrix
	return to_parent

# data bone hierarchy
def data_hierarchy(arma):
	# if rigify use
	if imm_static.getglobald("IS_RIGIFY"):
		return data_hierarchy_rigify(arma)
	#
	rt_list = []
	for index, item in enumerate(arma.bones):
		index_parent = get_index(item.parent, arma.bones)
		# check
		if index_parent >= index:
			print("--ATTENTION!--")
			print("imm export error: hierarchy wrong, child's index bigger than parent's")
			assert(False)
		rt_list.append([index, index_parent])
	return rt_list

# data offset transformation, mesh to armature
def data_offset(o_mesh, o_arma, arma):
	# all world transform should be zero and no scale.
	# otherwise mesh_to_arma matrix will be double influence to child mesh
	# because child mesh already has been modified by parent
	# thus mesh_to_arma shold be identity matrix
	# this step is unnecessary, but check if the world fransform is zero and no scale
	#
	# if rigify use
	if imm_static.getglobald("IS_RIGIFY"):
		return data_offset_rigify(o_mesh, o_arma, arma)
	#
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
	# if rigify use
	if imm_static.getglobald("IS_RIGIFY"):
		return data_anim_clip_rigify(scene, action, o_arma)
	# set active action
	o_arma.animation_data.action = action
	time_list = []
	pos_list = []
	sca_list = []
	rot_list = []
	# find completed framekeys in fcurves
	global anim_fcurve_keys_max
	anim_fcurve_keys_max = 0
	key_co_set = set()
	for ix_fcu in range(0, len(action.fcurves)):
		for key in action.fcurves[ix_fcu].keyframe_points:
			key_co_set.add(key.co[0])
	key_co_list = sorted(key_co_set)
	anim_fcurve_keys_max = len(key_co_list);
	# fps -> second
	frame_time = 1/scene.render.fps
	# time
	for bone in o_arma.pose.bones:
		for key_co in key_co_list:
			time_list.append(key_co*frame_time)
			pos_list.append(None)
			sca_list.append(None)
			rot_list.append(None)
	# position scale rotation
	len_key = len(key_co_list)
	for ix_key, key_co in enumerate(key_co_list):
		scene.frame_set(key_co)
		scene.update
		for ix, bone in enumerate(o_arma.data.bones):
			mat_to_p = get_to_parent(o_arma.pose.bones.get(bone.name)).transposed()
			mat_to_p = to_left_matrix(mat_to_p)
			mat_to_p = mat_to_p.transposed()
			loc, rot, sca = mat_to_p.decompose()
			rot = mathutils.Quaternion((rot.x, rot.y, rot.z, rot.w))
			pos_list[ix*len_key+ix_key] = loc
			sca_list[ix*len_key+ix_key] = sca
			rot_list[ix*len_key+ix_key] = rot
	return [time_list, pos_list, sca_list, rot_list]

# reassign weight and index
def reassign_weight(vert_group, redirect_group):
	re_list = []
	for group in vert_group:
		re_list.append([redirect_group[group.group], group.weight])
	re_list = sorted(re_list, key=lambda student: student[1], reverse=True)
	len_list = len(re_list)
	if len_list > 4:
		re_list = re_list[0:4]
	sum_weight = 0.0
	for re in re_list:
		sum_weight += re[1]
	sum_weight_diff = 1.0-sum_weight
	# sum_weight should be 1.0, or 0.0 for none influence
	# normalize
	if sum_weight_diff > 0.01 or sum_weight_diff < 0.01:
		for re in re_list:
			re[1] += (re[1]/sum_weight)*sum_weight_diff
	if len_list < 4:
		for ix in range(0, 4-len_list):
			re_list.append([0, 0.0])
	#
	return re_list

# data blender indices and weights
def data_ble_index_weight(mesh, o_mesh):
	# if rigify use
	if imm_static.getglobald("IS_RIGIFY"):
		return data_ble_index_weight_rigify(mesh, o_mesh)
	# get current group index map to armatrue index
	global anim_arma_list
	redirect_group = {}
	for index, gro in enumerate(o_mesh.vertex_groups):
		if gro.name not in anim_arma_list:
			print("--ATTENTION!--")
			print("imm export error: vertex group name not found in armature")
			print("imm export error: please ensure only one visible armature in scene")
			assert(False)
		redirect_group[index] = anim_arma_list.index(gro.name)
	#
	ble_index = []
	ble_weight = []
	for vert in mesh.vertices:
		ble_index.append([])
		ble_weight.append([])
		# only use 4 bone per vertex
		re_group = reassign_weight(vert.groups, redirect_group)
		for group in re_group:
			ble_index[-1].append(group[0])
			ble_weight[-1].append(group[1])
	return [ble_index, ble_weight]

# data blender indices and weights add according uv
def data_ble_index_weight_add(len_uv, uv_ex_dict, d_ble_index_weight):
	for ix in range(len_uv-len(uv_ex_dict), len_uv):
		d_ble_index_weight[0].append(d_ble_index_weight[0][uv_ex_dict[ix]])
		d_ble_index_weight[1].append(d_ble_index_weight[1][uv_ex_dict[ix]])
	return d_ble_index_weight

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
	global anim_fcurve_keys_max
	if anim_fcurve_keys_max == 0:
		print("--ATTENTION!--")
		print("imm export error: keyframes no date")
		assert(False)
	for ix in range(0, len(txt_time)):
		if ix%anim_fcurve_keys_max == 0:
			rt_list.append("B"+str(int(ix/anim_fcurve_keys_max))+" #K: "+str(anim_fcurve_keys_max)+" {")
		rt_list.append("T: "+txt_time[ix]+" P: "+txt_pos[ix]+" S: "+txt_sca[ix]+" Q: "+txt_rot[ix])
		if (ix-anim_fcurve_keys_max+1)%anim_fcurve_keys_max == 0:
			rt_list.append("}")
	return rt_list

# package vertex with animation data
def package_vertex_anim(len_uv, txt_position, txt_normal, txt_tangent, txt_uv, txt_ble_index, txt_ble_weight):
	rt_list = []
	for ix in range(0, len_uv):
		temp = "P: "+txt_position[ix]+"\n"
		temp += "T: "+txt_tangent[ix][0:-2]+"\n"
		temp += "N: "+txt_normal[ix]+"\n"
		temp += "T: "+txt_uv[ix]+"\n"
		temp += "W: "+txt_ble_weight[ix]+"\n"
		temp += "I: "+txt_ble_index[ix]+"\n"
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
		txt_pos = imm_static.format_vector(anim_clip[1])
		txt_sca = imm_static.format_vector(anim_clip[2])
		txt_rot = imm_static.format_vector(anim_clip[3])
		txt_anim_clip = package_anim_clip(txt_time, txt_pos, txt_sca, txt_rot)	
		txt_coll_anim_clip.append("AnimationClip "+action.name)
		txt_coll_anim_clip.append("{")
		txt_coll_anim_clip += txt_anim_clip
		txt_coll_anim_clip.append("}")
		len_anim_clip += 1
	# mesh data init
	txt_vertex = []
	txt_triangle = []
	sub_vertex_start = [0]
	sub_vertex_count = []
	sub_face_start = [0]
	sub_face_count = []
	txt_material = []
	# build mesh data
	for ix in objects_mesh:
		# arrange vertex accroding uv
		o_mesh = bpy.data.objects[ix]
		mesh = bpy.data.objects[ix].data		
		uv, uv_ex_dict, tessface = imm_static.data_uv_and_face(mesh)
		len_uv = len(uv)
		# triangle and vertex
		triangle = imm_static.data_triangle(tessface)
		position = imm_static.data_position(mesh, len_uv, uv_ex_dict)
		normal = imm_static.data_normal(mesh, len_uv, uv_ex_dict)
		tangent = imm_static.data_tangent(len_uv, position, normal, uv, triangle)
		# vertex
		txt_uv = imm_static.format_vector(uv)
		txt_position = imm_static.format_vector(position)
		txt_normal = imm_static.format_vector(normal)
		txt_tangent = imm_static.format_vector(tangent)
		# subset
		sub_vertex_count.append(len_uv)
		sub_face_count.append(len(triangle))
		if len(sub_vertex_count) > 1:
			sub_vertex_start.append(sub_vertex_start[-1]+sub_vertex_count[-2])
			sub_face_start.append(sub_face_start[-1]+sub_face_count[-2])
			triangle = imm_static.offset_triangle(triangle, sub_vertex_start[-1])
		txt_triangle += imm_static.format_triangle(triangle)
		# material
		txt_material += imm_static.txt_matrial(mesh)
		# bone weight and index
		ble_index_weight = data_ble_index_weight(mesh, o_mesh)
		ble_index_weight = data_ble_index_weight_add(len_uv, uv_ex_dict, ble_index_weight)
		txt_ble_index = format_index(ble_index_weight[0])
		txt_ble_weight = imm_static.format_vector(ble_index_weight[1])
		txt_vertex += package_vertex_anim\
			(len_uv, txt_position, txt_normal, txt_tangent, txt_uv, txt_ble_index, txt_ble_weight)
	# subset table
	txt_subset = []
	for ix in range(0, len(sub_vertex_start)):
		temp_str = "SubsetID: "+str(ix)+" "
		temp_str += "VertexStart: "+str(sub_vertex_start[ix])+" "
		temp_str += "VertexCount: "+str(sub_vertex_count[ix])+" "
		temp_str += "FaceStart: "+str(sub_face_start[ix])+" "
		temp_str += "FaceCount: "+str(sub_face_count[ix])
		txt_subset.append(temp_str)
	txt_subset.append("")
	return [txt_vertex, txt_triangle, txt_subset, txt_material, \
		txt_offset, txt_hierarchy, txt_coll_anim_clip, len_anim_clip]

# package bone offset hierarchy animation clips
def package_bone_anim(offset, hierarchy, coll_anim_clip):
	txt_anim = [""]
	txt_anim.append("--------------------------------BoneOffsets-")
	txt_anim += offset
	txt_anim.append("")
	txt_anim.append("------------------------------BoneHierarchy-")
	txt_anim += hierarchy
	txt_anim.append("")
	txt_anim.append("-----------------------------AnimationClips-")
	txt_anim += coll_anim_clip
	return txt_anim

# export m3d anim
def export_m3d_anim():
	time_start = datetime.datetime.now()
	# object
	objects_arma = imm_static.find_first_object("ARMATURE")
	objects_mesh = imm_static.find_mesh()
	scene = bpy.data.scenes[0]
	coll_action = bpy.data.actions
	# check
	if len(objects_mesh) == 0:
		print("imm export error: no uv mapped mesh found")
		return;
	if len(objects_arma) == 0:
		print("imm export error: no armature found")
		return
	if len(coll_action) == 0:
		print("imm export error: no action found")
		return
	# object
	o_arma = bpy.data.objects[objects_arma[0]]
	arma = o_arma.data
	build_arma_info(o_arma, arma)
	# if rigify use
	if not imm_static.getglobald("IS_RIGIFY"):
		imm_static.set_global_dict("IS_RIGIFY", is_rigify(arma))
	if imm_static.getglobald("IS_RIGIFY"):
		read_hierarchy_rigify(arma)
	global anim_len_bones
	# package
	txt_vertex, txt_triangle, txt_subset, txt_material, \
		txt_offset, txt_hierarchy, txt_coll_anim_clip, len_anim_clip = \
		package_mesh_anim(scene, objects_mesh, o_arma, arma, coll_action)
	txt_m3d = imm_static.package_m3d([txt_vertex, txt_triangle, txt_subset, txt_material], \
		[anim_len_bones, len_anim_clip])
	txt_m3d += package_bone_anim(txt_offset, txt_hierarchy, txt_coll_anim_clip)
	file_name = bpy.path.basename(bpy.context.blend_data.filepath)
	file_name = file_name.replace(".blend", "")
	export = imm_static.getglobald("EXPORT_DIR")+file_name+".m3d"
	imm_static.write_text(export, txt_m3d)
	time_spend = datetime.datetime.now()-time_start
	# print
	print("-----------------------")
	print("M3D Export (Animation):")
	print("-----------------------")
	print("left hand:  "+str(imm_static.getglobald("IS_LEFT_HAND")))
	print("is rigify:  "+str(imm_static.getglobald("IS_RIGIFY")))
	print("export:     "+export)
	print("spend time: "+str(time_spend.total_seconds())+" seconds")

# run stript
def run_script():
	is_export_anim = imm_static.getglobald("IS_EXPORT_ANIM")
	if (is_export_anim):
		export_m3d_anim()
	else:
		imm_static.export_m3d()

# end

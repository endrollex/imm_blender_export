#
# animation_export.py
# export animation data to text
#
import os
import copy
import bpy
import mathutils
import sys
sys.path.append("C:\\Dropbox\\imm_blender_export\\")
import static_export
os.system("cls")

# setting
is_left_hand = True
export_dir = static_export.export_dir
static_export.is_left_hand = is_left_hand

# refer
o_arma = bpy.data.objects[0]
o_mesh = bpy.data.objects[2]
arma = o_arma.data
mesh = o_mesh.data
scene = bpy.data.scenes[0]
action = bpy.data.actions[0]

# matrix right to left hand
def to_left_matrix(mat):
	s_x = mathutils.Matrix.Identity(3)
	s_x[0][0] = -1
	mat_l = mat.to_3x3()
	mat_l = s_x*mat_l*s_x
	mat_l = mat_l.to_4x4()
	mat_l[3][0:3] = -mat[3][0], mat[3][1], mat[3][2]
	return mat_l

# matrix right to left hand
def to_left_matrix_b(mat):
	mat_l = mathutils.Matrix()
	mat_l[0][0:3] = mat[0][0], -mat[0][1], -mat[0][2]
	mat_l[1][0:3] = -mat[1][0], mat[1][1], mat[1][2]
	mat_l[2][0:3] = -mat[2][0], mat[2][1], mat[2][2]
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
		if is_left_hand:
			mat = to_left_matrix(mat)
		mat = mat.inverted()
		rt_list.append(mat)
	return rt_list

# data time position scale rotation
def data_time_p_s_r():
	time_list = []
	pos_list = []
	sca_list = []
	rot_list = []
	# find completed framekeys in fcurves
	fcurve_keys_max = 0
	fcurve_ix = 0
	for ix_fcu in range(0, len(action.fcurves)):
		len_fcurve_keys = len(action.fcurves[ix_fcu].keyframe_points)
		if len_fcurve_keys > fcurve_keys_max:
			fcurve_keys_max = len_fcurve_keys
			fcurve_ix = ix_fcu
	print("keyframes:\t"+str(fcurve_keys_max))
	# fps -> second
	frame_time = 1/scene.render.fps
	cnt_bone = 0
	# time
	for bone in o_arma.pose.bones:
		for key in action.fcurves[fcurve_ix].keyframe_points:
			time_list.append(key.co[0]*frame_time)
			pos_list.append(0)
			sca_list.append(0)
			rot_list.append(0)
		cnt_bone += 1
	# position scale rotation
	for ix_key, key in enumerate(action.fcurves[fcurve_ix].keyframe_points):
		len_key = len(action.fcurves[fcurve_ix].keyframe_points)
		scene.frame_set(key.co[0])
		scene.update
		for ix in range(0, cnt_bone):
			mat_to_p = get_to_parent(ix).transposed()
			mat_to_p = to_left_matrix(mat_to_p)
			mat_to_p = mat_to_p.transposed()
			loc, rot, sca = mat_to_p.decompose()
			rot = mathutils.Quaternion((rot.x, rot.y, rot.z, rot.w))
			pos_list[ix*len_key+ix_key] = loc
			sca_list[ix*len_key+ix_key] = sca
			rot_list[ix*len_key+ix_key] = rot
	return [time_list, pos_list, sca_list, rot_list]

# data blender indices and weights
def data_b_index_weight():
	b_index = []
	b_weight = []
	for vert in mesh.vertices:
		b_index.append([])
		b_weight.append([])
		cnt_less4 = 4-len(vert.groups)
		cnt_group = 0
		for group in vert.groups:
			if cnt_group > 3:
				break
			b_index[-1].append(group.group)
			b_weight[-1].append(group.weight)
			cnt_group += 1
		for ix in range(0, cnt_less4):
			b_index[-1].append(0)
			b_weight[-1].append(0.0)
	return [b_index, b_weight]

# data blender indices and weights add according uv
def data_b_index_weight_add(len_uv, uv_ex_dict, d_b_index_weight):
	for ix in range(len_uv-len(uv_ex_dict), len_uv):
		d_b_index_weight[0].append(d_b_index_weight[0][uv_ex_dict[ix]])
		d_b_index_weight[1].append(d_b_index_weight[1][uv_ex_dict[ix]])
	return d_b_index_weight

# package hierarchy
def package_hierarchy(list_in):
	rt_list = []
	for index in list_in:
		rt_list.append("ParentIndexOfBone"+str(index[0])+": "+str(index[1]))
	return rt_list

# package offset
def package_offset(list_in):
	rt_list = []
	for ix in range(0, len(list_in)):
		rt_list.append("BoneOffset"+str(ix)+" "+list_in[ix])
	return rt_list

# package time position scale rotation
def package_time_p_s_r(txt_time, txt_pos, txt_sca, txt_rot):
	rt_list = []
	for ix in range(0, len(txt_time)):
		rt_list.append("Time: "+txt_time[ix]+" Pos: "+txt_pos[ix]+" Scale: "+txt_sca[ix]+" Quat: "+txt_rot[ix])
	return rt_list	

# package vertex with animation data
def package_vertex2(len_uv, txt_position, txt_normal, txt_tangent, txt_uv, txt_b_index, txt_b_weight):
	rt_list = []
	for ix in range(0, len_uv):
		temp = "Position: "+txt_position[ix]+"\n"
		temp += "Tangent: "+txt_tangent[ix][0:-2]+"\n"
		temp += "Normal: "+txt_normal[ix]+"\n"
		temp += "TexCoord: "+txt_uv[ix]+"\n"
		temp += "BlendWeights: "+txt_b_weight[ix]+"\n"
		temp += "BlendIndices: "+txt_b_index[ix]+"\n"
		rt_list.append(temp)
	return rt_list

# export m3d anim format parts
def export_m3d_anim():
	print("-------------------")
	print("Export information:")
	print("-------------------")
	# get data and format them
	d_offset = data_offset()
	d_hierarchy = data_hierarchy()
	d_time_p_s_r = data_time_p_s_r()
	d_b_index_weight = data_b_index_weight()
	txt_offset = package_offset(format_matrix(d_offset))
	txt_hierarchy = package_hierarchy(d_hierarchy)
	txt_time = number_to_str(d_time_p_s_r[0])
	txt_pos = static_export.format_vector(d_time_p_s_r[1])
	txt_sca = static_export.format_vector(d_time_p_s_r[2])
	txt_rot = static_export.format_vector(d_time_p_s_r[3])
	txt_time_p_s_r = package_time_p_s_r(txt_time, txt_pos, txt_sca, txt_rot)
	# arrange vertex accroding uv
	d_uv_and_face = static_export.data_uv_and_face()
	len_uv = len(d_uv_and_face[0])
	d_triangle = static_export.data_triangle(d_uv_and_face[2])
	d_position = static_export.data_position(len_uv, d_uv_and_face[1])
	d_normal = static_export.data_normal(len_uv, d_uv_and_face[1])
	d_tangent = static_export.data_tangent(len_uv, d_position, d_normal, d_uv_and_face[0], d_triangle)
	txt_uv = static_export.format_vector(d_uv_and_face[0])
	txt_triangle = static_export.format_triangle(d_triangle)
	txt_position = static_export.format_vector(d_position)
	txt_normal = static_export.format_vector(d_normal)
	txt_tangent = static_export.format_vector(d_tangent)
	# bone weight and index
	d_b_index_weight = data_b_index_weight_add(len_uv, d_uv_and_face[1], d_b_index_weight)
	txt_b_index = format_index(d_b_index_weight[0])
	txt_b_weight = static_export.format_vector(d_b_index_weight[1])
	txt_vertex = package_vertex2(len_uv, txt_position, txt_normal, txt_tangent, txt_uv, txt_b_index, txt_b_weight)
	# export text
	export = export_dir+"export_offset.txt"
	static_export.write_text(export, txt_offset)
	export = export_dir+"export_hierarchy.txt"
	static_export.write_text(export, txt_hierarchy)
	export = export_dir+"export_time_p_s_r.txt"
	static_export.write_text(export, txt_time_p_s_r)
	export = export_dir+"export_vertex_a.txt"
	static_export.write_text(export, txt_vertex)
	print("left hand:\t"+str(is_left_hand))
	print("export dir:\t"+export_dir)
	print("bones:\t\t"+str(len(arma.bones)))

# main
export_m3d_anim()

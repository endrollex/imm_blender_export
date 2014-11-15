#
# static_export.py
# export static data to text
#
import os
import copy
import bpy
import math
import mathutils
os.system("cls")

# refer
mesh = bpy.data.meshes[0]

# setting export dir
export_dir = "D:\\Dropbox\\imm_blender_export\\"
is_left_hand = False

# round sig
def round_sig(x, sig = 6):
	if x < 1e-100 and x > -1e-100:
		return 0.0
	if x < 0:
		return round_sig(-x, sig)*-1
	return round(x, sig-int(math.floor(math.log10(x)))-1)

# prepare uv function
def prepare_uv():
	# check tessfaces, to avoid repeated calc_tessface
	if len(mesh.tessfaces) == 0:
		mesh.calc_tessface()
	# check uv is exists or not
	try:
		mesh.tessface_uv_textures[0].data
	except:
		return False
	return True

# write text
def write_text(path, data_list):
	fw = open(path, "w")
	data_str = ""
	for one in data_list:
		data_str += one+"\n"
	fw.write(data_str)
	fw.close()

# right hand to left hand vector3
# mirrored along the YZ plane in left hand
def to_left_hand_vec3(vec3_in):
	return mathutils.Vector((-vec3_in.x, vec3_in.y, vec3_in.z))

# if left hand, flip uv along X
def uv_flip_x(vec2_in):
	return mathutils.Vector((vec2_in.x, 1-vec2_in.y)) if is_left_hand else vec2_in

# coordinate to string
def coordinate_to_str(list_in):
	str_out = str(round_sig(list_in[0]))
	for ix in range(1, len(list_in)):
		str_out = str_out+" "+str(round_sig(list_in[ix]))
	return str_out

# format vector
def format_vector(list_in):
	rt_list = []
	for l in list_in:
		rt_list.append(coordinate_to_str(l))
	return rt_list

# format triangle
def format_triangle(list_in):
	rt_list = []
	for t in list_in:
		rt_list.append(str(t[0])+" "+str(t[1])+" "+str(t[2]))
	return rt_list

# get uv list and tessface list
# Blender's uv is per tessface
# we need uv per vertex
def data_uv_and_face():
	# store vertex of tessface
	tessface_list = []
	# check tessfaces, to avoid repeated calc_tessface
	if len(mesh.tessfaces) == 0:
		mesh.calc_tessface()
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
	uv_temp = ["", "", "", ""]
	for ix in range(0, len(uv_data)):
		v = len(uv_data[ix].uv)
		uv_temp[0] = copy.deepcopy(uv_flip_x(uv_data[ix].uv1))
		uv_temp[1] = copy.deepcopy(uv_flip_x(uv_data[ix].uv2))
		uv_temp[2] = copy.deepcopy(uv_flip_x(uv_data[ix].uv3))
		if v == 4:
			uv_temp[3] = copy.deepcopy(uv_flip_x(uv_data[ix].uv4))
		for iv in range(0, v):
			if uv_temp[iv] not in uv_list[tessface_list[ix][iv]]:
				uv_list[tessface_list[ix][iv]].append(uv_temp[iv])
				if len(uv_list[tessface_list[ix][iv]]) > 1:
					uv_list.append([uv_temp[iv]])
					# uv_ex_dict_inv: which vertex index is mapping second uv
					uv_ex_dict_inv.fromkeys([tessface_list[ix][iv]])
					uv_ex_dict_inv[tessface_list[ix][iv]] = len(uv_list)-1					
					# uv_ex_dict: uv index (exceed vertex count) is mapping vertex index
					uv_ex_dict.fromkeys([len(uv_list)-1])
					uv_ex_dict[len(uv_list)-1] = tessface_list[ix][iv]
					tessface_list[ix][iv] = len(uv_list)-1
				if len(uv_list[tessface_list[ix][iv]]) > 2:
					return ["one vertex has more than two uv, out of the current solution"]
			else:
				if uv_temp[iv] != uv_list[tessface_list[ix][iv]][0]:
					tessface_list[ix][iv] = uv_ex_dict_inv[tessface_list[ix][iv]]
	# build uv list
	temp = uv_list
	uv_list = []
	for t in temp:
		uv_list.append(t[0])
	return [uv_list, uv_ex_dict, tessface_list]

# polygons tangent
# it can not use, just for test
def data_tangent_p(len_uv, uv_ex_dict):
	rt_list = []
	for ix in range(0, len_uv):
		rt_list.append(mathutils.Vector((0.0, 0.0, 0.0, 1.0)))
	mesh.calc_tangents()
	for poly in mesh.polygons:
		for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
			vi = mesh.loops[loop_index].vertex_index
			t = to_left_hand_vec3(mesh.loops[loop_index].tangent)
			b = mesh.loops[loop_index].bitangent_sign
			rt_list[vi].xyz = t.xyz
			rt_list[vi].w = b
	for u in uv_ex_dict:
		rt_list[u] = rt_list[uv_ex_dict[u]]
	return rt_list

# tangent list
# polygons tangent is not corresponding with tessface
# it is needed to compute per-vertex tangent spaces for an arbitrary triangle mesh
# Algorithm from Mathematics for 3D Game Programming and Computer Graphics, 3rd ed. Listing 7.1
def data_tangent(len_uv, position_list, normal_list, uv_list, triangle_list):
	tan1 = []
	tan2 = []
	for ix in range(0, len_uv):
		tan1.append(mathutils.Vector((0.0, 0.0, 0.0)))
		tan2.append(mathutils.Vector((0.0, 0.0, 0.0)))
	for ix in range(0, len(triangle_list)):
		i1 = triangle_list[ix][0]
		i2 = triangle_list[ix][1]
		i3 = triangle_list[ix][2]
		v1 = position_list[i1]
		v2 = position_list[i2]
		v3 = position_list[i3]
		w1 = uv_list[i1]
		w2 = uv_list[i2]
		w3 = uv_list[i3]
		#
		x1 = v2.x - v1.x
		x2 = v3.x - v1.x
		y1 = v2.y - v1.y
		y2 = v3.y - v1.y
		z1 = v2.z - v1.z
		z2 = v3.z - v1.z
		#
		s1 = w2.x - w1.x
		s2 = w3.x - w1.x
		t1 = w2.y - w1.y
		t2 = w3.y - w1.y
		# if div zero error
		r = 0
		test = s1 * t2 - s2 * t1
		if test == 0:
			print("error: div zero, uv may be wrong")
		else:
			r = 1.0 / test
		sdir = mathutils.Vector(((t2 * x1 - t1 * x2) * r, (t2 * y1 - t1 * y2) * r, (t2 * z1 - t1 * z2) * r))
		tdir = mathutils.Vector(((s1 * x2 - s2 * x1) * r, (s1 * y2 - s2 * y1) * r, (s1 * z2 - s2 * z1) * r))
		tan1[i1] += sdir
		tan1[i2] += sdir
		tan1[i3] += sdir
		tan2[i1] += tdir
		tan2[i2] += tdir
		tan2[i3] += tdir
	#
	tangent = []
	for ix in range(0, len_uv):
		n = normal_list[ix]
		t = tan1[ix]
		tangent.append(mathutils.Vector((0.0, 0.0, 0.0, 1.0)))
		# Gram-Schmidt orthogonalize.
		tangent[ix].xyz = ((t - n * n.dot(t)).normalized()).xyz
		# Calculate handedness.
		tangent[ix].w = -1.0 if (n.cross(t)).dot(tan2[ix]) < 0.0 else 1.0
	# dummy tangent
	#for ix in range(0, len_uv):
	#	tangent[ix] = mathutils.Vector((0.0, 0.0, 0.0, 1.0))
	return tangent
	
# triangle list
def data_triangle(tessface_list):
	rt_list = []
	for t in tessface_list:
		rt_list.append([t[0], t[2], t[1]]) if is_left_hand else rt_list.append([t[0], t[1], t[2]])
		if len(t) == 4:
			rt_list.append([t[0], t[3], t[2]]) if is_left_hand else rt_list.append([t[0], t[2], t[3]])
	return rt_list

# position list
def data_position(len_uv, uv_ex_dict):
	rt_list = []
	for v in mesh.vertices:
		rt_list.append(to_left_hand_vec3(v.co) if is_left_hand else v.co)
	for ix in range(len_uv-len(uv_ex_dict), len_uv):
		rt_list.append(rt_list[uv_ex_dict[ix]])
	return rt_list

# normal list
def data_normal(len_uv, uv_ex_dict):
	rt_list = []
	for v in mesh.vertices:
		rt_list.append(to_left_hand_vec3(v.normal) if is_left_hand else v.normal)
	for ix in range(len_uv-len(uv_ex_dict), len_uv):
		rt_list.append(rt_list[uv_ex_dict[ix]])
	return rt_list

# package vertex
def package_vertex(len_uv, txt_position, txt_normal, txt_tangent, txt_uv):
	rt_list = []
	for ix in range(0, len_uv):
		temp = "Position: "+txt_position[ix]+"\n"
		temp += "Tangent: "+txt_tangent[ix][0:-2]+"\n"
		temp += "Normal: "+txt_normal[ix]+"\n"
		temp += "TexCoord: "+txt_uv[ix]+"\n"
		rt_list.append(temp)
	return rt_list

# export m3d format parts
def export_m3d():
	d_uv_and_face = data_uv_and_face()
	len_uv = len(d_uv_and_face[0])
	d_triangle = data_triangle(d_uv_and_face[2])
	d_position = data_position(len_uv, d_uv_and_face[1])
	d_normal = data_normal(len_uv, d_uv_and_face[1])
	d_tangent = data_tangent(len_uv, d_position, d_normal, d_uv_and_face[0], d_triangle)
	txt_uv = format_vector(d_uv_and_face[0])
	txt_triangle = format_triangle(d_triangle)
	txt_position = format_vector(d_position)
	txt_normal = format_vector(d_normal)
	txt_tangent = format_vector(d_tangent)
	txt_vertex = package_vertex(len_uv, txt_position, txt_normal, txt_tangent, txt_uv)
	# write
	export = export_dir+"export_vertex.txt"
	write_text(export, txt_vertex)
	export = export_dir+"export_triangle.txt"
	write_text(export, txt_triangle)
	print("-------------------")
	print("Export information:")
	print("-------------------")
	print("vertices:\t"+str(len_uv))
	print("triangles:\t"+str(len(txt_triangle)))
	print("export dir:\t"+export_dir)

# main
if prepare_uv():
	export_m3d()
else:
	print("export error, uv is not prepared")
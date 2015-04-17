#
# export_static.py
# export static data to text
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#
import os
import bpy
import math
import mathutils
import datetime
import sys
sys.path.append("D:\\Dropbox\\imm_blender_export\\")
import global_var
#os.system("cls")

####################################################################################################
# format functions
####################################################################################################
####################################################################################################

# round sig
def round_sig(x, sig = 6):
	if x < 1e-100 and x > -1e-100:
		return 0.0
	if x < 0:
		return round_sig(-x, sig)*-1
	return round(x, sig-int(math.floor(math.log10(x)))-1)

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
	if not global_var.is_left_hand:
		return mathutils.Vector((vec3_in.x, vec3_in.y, vec3_in.z))
	return mathutils.Vector((-vec3_in.x, vec3_in.y, vec3_in.z))

# if left hand, flip uv along X
def uv_flip_x(vec2_in):
	if global_var.is_left_hand:
		return mathutils.Vector((vec2_in.x, 1-vec2_in.y))
	return mathutils.Vector((vec2_in.x, vec2_in.y))

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

# offset triangle
def offset_triangle(list_in, offset):
	rt_list = []
	for t in list_in:
		rt_list.append([t[0]+offset, t[1]+offset, t[2]+offset])
	return rt_list

####################################################################################################
# mesh functions
####################################################################################################
####################################################################################################

# calc_tess
def calc_tess(mesh):
	if len(mesh.tessfaces) == 0:
		mesh.calc_tessface()

# find_mesh, mesh which must has uv
def find_mesh():
	obj_list = []
	for ix, obj in enumerate(bpy.data.objects):
		if obj.type == "MESH":
			mesh = bpy.data.objects[ix].data
			calc_tess(mesh)
			if len(mesh.uv_textures) != 0 and not obj.hide:
				obj_list.append(ix)
	return obj_list

# find_first_object
def find_first_object(o_type):
	for ix, obj in enumerate(bpy.data.objects):
		if obj.type == o_type and not obj.hide:
			return [ix]
	return []

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
		if (len(t)) == 0:
			print("--ATTENTION!--")
			print("imm export error: uv wrong, maybe has single vertex")
			assert(False)
		uv_list.append(t[0])
	return [uv_list, uv_ex_dict, tessface_list]

# get tangent list
# Blender's polygons tangent is not corresponding with tessface
# it is needed to compute per-vertex tangent
# Algorithm from Mathematics for 3D Game Programming and Computer Graphics, 3rd ed. Listing 7.1
# test sometimes will div by zero, i do not know why
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
		# if div by zero error??
		r = 0
		test = s1 * t2 - s2 * t1
		if test == 0:
			None
			#print("imm export error: div by zero, uv may be wrong")
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
	return tangent

# get triangle list
def data_triangle(tessface_list):
	rt_list = []
	for t in tessface_list:
		rt_list.append([t[0], t[2], t[1]]) if global_var.is_left_hand else rt_list.append([t[0], t[1], t[2]])
		if len(t) == 4:
			rt_list.append([t[0], t[3], t[2]]) if global_var.is_left_hand else rt_list.append([t[0], t[2], t[3]])
	return rt_list

# get position list
def data_position(mesh, len_uv, uv_ex_dict):
	rt_list = []
	for v in mesh.vertices:
		rt_list.append(to_left_hand_vec3(v.co))
	for ix in range(len_uv-len(uv_ex_dict), len_uv):
		rt_list.append(rt_list[uv_ex_dict[ix]])
	return rt_list

# get normal list
def data_normal(mesh, len_uv, uv_ex_dict):
	rt_list = []
	for v in mesh.vertices:
		rt_list.append(to_left_hand_vec3(v.normal))
	for ix in range(len_uv-len(uv_ex_dict), len_uv):
		rt_list.append(rt_list[uv_ex_dict[ix]])
	return rt_list

# get matrial
def txt_matrial(mesh):
	rt_list = []
	# materials
	ambient = 1.0
	diffuse = mathutils.Vector((0.64, 0.64, 0.64))
	specular = mathutils.Vector((0.5, 0.5, 0.5))
	mat_hard = 12.298
	reflect = mathutils.Vector((0.0, 0.0, 0.0))
	diffuse_map = mesh.name+".dds"
	normal_map = mesh.name+"_nrm.dds"
	if (len(mesh.materials)) != 0:
		mat = mesh.materials[0]
		ambient = mat.ambient
		diffuse = mat.diffuse_color*mesh.materials[0].diffuse_intensity
		specular = mat.specular_color*mesh.materials[0].specular_intensity
		# mat_hard method from export_fbx.py
		mat_hard = ((float(mat.specular_hardness) - 1.0) / 510.0) * 128.0
		reflect = mat.mirror_color*mat.raytrace_mirror.reflect_factor
	# materials txt
	rt_list.append("Ambient:"+(" "+str(ambient))*3)
	rt_list.append("Diffuse: "+str(coordinate_to_str(diffuse)))
	rt_list.append("Specular: "+str(coordinate_to_str(specular)))
	rt_list.append("SpecPower: "+str(round_sig(mat_hard)))
	rt_list.append("Reflectivity: "+str(coordinate_to_str(reflect)))
	rt_list.append("AlphaClip: 0")
	rt_list.append("Effect: Normal")
	rt_list.append("DiffuseMap: "+diffuse_map)
	rt_list.append("NormalMap: "+normal_map)
	rt_list.append("")
	return rt_list

####################################################################################################
# export functions
####################################################################################################
####################################################################################################

# package vertex
def package_vertex(len_uv, txt_position, txt_normal, txt_tangent, txt_uv):
	rt_list = []
	for ix in range(0, len_uv):
		temp = "P: "+txt_position[ix]+"\n"
		temp += "T: "+txt_tangent[ix][0:-2]+"\n"
		temp += "N: "+txt_normal[ix]+"\n"
		temp += "T: "+txt_uv[ix]+"\n"
		rt_list.append(temp)
	return rt_list

# package mesh static
def package_mesh_static(objects_mesh):
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
		mesh = bpy.data.objects[ix].data
		uv, uv_ex_dict, tessface = data_uv_and_face(mesh)
		len_uv = len(uv)
		# triangle and vertex
		triangle = data_triangle(tessface)
		position = data_position(mesh, len_uv, uv_ex_dict)
		normal = data_normal(mesh, len_uv, uv_ex_dict)
		tangent = data_tangent(len_uv, position, normal, uv, triangle)
		# vertex package
		txt_uv = format_vector(uv)
		txt_position = format_vector(position)
		txt_normal = format_vector(normal)
		txt_tangent = format_vector(tangent)
		txt_vertex += package_vertex(len_uv, txt_position, txt_normal, txt_tangent, txt_uv)
		# subset
		sub_vertex_count.append(len_uv)
		sub_face_count.append(len(triangle))
		if len(sub_vertex_count) > 1:
			sub_vertex_start.append(sub_vertex_start[-1]+sub_vertex_count[-2])
			sub_face_start.append(sub_face_start[-1]+sub_face_count[-2])
			triangle = offset_triangle(triangle, sub_vertex_start[-1])
		txt_triangle += format_triangle(triangle)
		# material
		txt_material += txt_matrial(mesh)
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
	return [txt_vertex, txt_triangle, txt_subset, txt_material]

# package m3d
def package_m3d(package_txt, info_anim = []):
	# mesh
	txt_vertex, txt_triangle, txt_subset, txt_material = package_txt
	len_bones = 0
	len_anim_clips = 0
	if (len(info_anim) == 2):
		len_bones, len_anim_clips = info_anim
	len_uv = len(txt_vertex)
	len_triangle = len(txt_triangle)
	len_subset = len(find_mesh())
	# m3d file header
	txt_m3d = []
	txt_m3d.append("---------------------------M3D_File_Header-")
	txt_m3d.append("Materials "+str(len_subset))
	txt_m3d.append("Vertices "+str(len_uv))
	txt_m3d.append("Triangles "+str(len_triangle))
	txt_m3d.append("Bones "+str(len_bones))
	txt_m3d.append("AnimationClips "+str(len_anim_clips))
	txt_m3d.append("")
	# materials
	txt_m3d.append("----------------------------------Materials-")
	txt_m3d += txt_material
	# subset table
	txt_m3d.append("-------------------------------Subset_Table-")
	txt_m3d += txt_subset
	# vertices
	txt_m3d.append("-----------------------------------Vertices-")
	txt_m3d += txt_vertex
	# triangles
	txt_m3d.append("----------------------------------Triangles-")
	txt_m3d += txt_triangle
	return txt_m3d

# export m3d static format
def export_m3d():
	time_start = datetime.datetime.now()
	objects_mesh = find_mesh()
	# check
	if len(objects_mesh) == 0:
		print("imm export error: no uv mapped mesh found")
		return;	
	txt_m3d = package_m3d(package_mesh_static(objects_mesh))
	export = global_var.export_dir+"export_static.txt"
	write_text(export, txt_m3d)
	time_spend = datetime.datetime.now()-time_start
	#
	print("--------------------")
	print("M3D Export (Static):")
	print("--------------------")
	print("left hand:\t"+str(global_var.is_left_hand))
	print("export dir:\t"+global_var.export_dir)
	print("spend time:\t"+str(time_spend.total_seconds())+" seconds")

# end

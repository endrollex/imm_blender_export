#
# export_static.py
# export static model data to text
#
import os
import bpy
import math
os.system("cls")
mesh = bpy.data.meshes[0]
mesh.calc_tessface()

# setting export dir
export_dir = "D:\\Dropbox\\imm_blender_export\\"

# round sig
def round_sig(x, sig = 6):
	if x < 1e-100 and x > -1e-100:
		return 0.0
	if x < 0:
		return round_sig(-x, sig)*-1
	return round(x, sig-int(math.floor(math.log10(x)))-1)

# prepare uv function
def prepare_uv():
	try:
		temp = mesh.tessface_uv_textures[0].data
		mesh.calc_tangents()
	except:
		return False
	return True

# write text
def write_text(path, info_list):
	fw = open(path, "w")
	info_str = ""
	for one in info_list:
		info_str += one+"\n"
	fw.write(info_str)
	fw.close()

# float format
def float_format(list_in):
	str_out = str(round_sig(list_in[0]))
	for ix in range(1, len(list_in)):
		str_out = str_out+" "+str(round_sig(list_in[ix]))
	return str_out

# uv per face
def get_face_and_uv():
	# store vertex of tessface
	face_list = []
	for t in mesh.tessfaces:
			face_list.append(t.vertices)
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
		uv_temp[0] = float_format(uv_data[ix].uv1)
		uv_temp[1] = float_format(uv_data[ix].uv2)
		uv_temp[2] = float_format(uv_data[ix].uv3)
		if v == 4:
			uv_temp[3] = float_format(uv_data[ix].uv4)
		for iv in range(0, v):
			if uv_temp[iv] not in uv_list[face_list[ix][iv]]:
				uv_list[face_list[ix][iv]].append(uv_temp[iv])
				if len(uv_list[face_list[ix][iv]]) > 1:
					uv_list.append([uv_temp[iv]])
					# dict for original vertex index map new vertex index
					uv_ex_dict_inv.fromkeys([face_list[ix][iv]])
					uv_ex_dict_inv[face_list[ix][iv]] = len(uv_list)-1					
					# indicate one vertex have two uv
					uv_ex_dict.fromkeys([len(uv_list)-1])
					uv_ex_dict[len(uv_list)-1] = face_list[ix][iv]
					face_list[ix][iv] = len(uv_list)-1
				if len(uv_list[face_list[ix][iv]]) > 2:
					return ["one vertex have more than two uv, exceed the current solution"]
			else:
				if uv_temp[iv] != uv_list[face_list[ix][iv]][0]:
					face_list[ix][iv] = uv_ex_dict_inv[face_list[ix][iv]]
	return [face_list, uv_list, uv_ex_dict]

# export triangle list
def get_triangle(face_list):
	rt_list = []
	for t in face_list:
		rt_list.append(str(t[0])+" "+str(t[1])+" "+str(t[2]))
		if len(t) == 4:
			rt_list.append(str(t[0])+" "+str(t[2])+" "+str(t[3]))
	return rt_list	

# export position
def get_position(face_list, uv_len, uv_ex_dict):
	rt_list = []	
	for v in mesh.vertices:
		temp = float_format(v.co)
		rt_list.append(temp)
	for ix in range(uv_len-len(uv_ex_dict), uv_len):
		rt_list.append(rt_list[uv_ex_dict[ix]])
	return rt_list

# export normal
def get_normal(face_list, uv_len, uv_ex_dict):
	rt_list = []	
	for v in mesh.vertices:
		temp = float_format(v.normal)
		rt_list.append(temp)
	for ix in range(uv_len-len(uv_ex_dict), uv_len):
		rt_list.append(rt_list[uv_ex_dict[ix]])
	return rt_list

# main
def main():
	face_and_uv = get_face_and_uv()
	uv_len = len(face_and_uv[1])
	g_triangle = get_triangle(face_and_uv[0])
	g_position = get_position(face_and_uv[0], uv_len, face_and_uv[2])
	g_normal = get_normal(face_and_uv[0], uv_len, face_and_uv[2])
	g_tangent = []
	for ix in range(0, uv_len):
		g_tangent.append("0.0 0.0 0.0 1")
	str_out = []
	for ix in range(0, uv_len):
		temp = "Position: "+g_position[ix]+"\n"
		temp += "Tangent: "+g_tangent[ix]+"\n"
		temp += "Normal: "+g_normal[ix]+"\n"
		temp += "Tex-Coords: "+face_and_uv[1][ix][0]+"\n"
		str_out.append(temp)
	export = export_dir+"export_v.txt"
	write_text(export, str_out)
	export = export_dir+"export_t.txt"
	write_text(export, g_triangle)
	print("-------------------")
	print("Export information:")
	print("-------------------")
	print("Vertices:\t"+str(uv_len))
	print("Triangles:\t"+str(len(g_triangle)))
	print("Export dir:\t"+export_dir)

# main prepare
if prepare_uv():
	main()
else:
	print("error, uv is not prepared")
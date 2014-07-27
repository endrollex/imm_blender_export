#
# export_static.py
# export static model data to text
#
import os
import bpy
os.system("cls")
mesh = bpy.data.meshes[0]
mesh.calc_tessface()

# setting export dir
export_dir = "D:\\Dropbox\\imm_blender_export\\"

# check stat
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

# str_format
def str_format(str_inout):
	str_inout = str_inout.replace("<Vector (", "")
	str_inout = str_inout.replace(")>", "")
	str_inout = str_inout.replace(",", "")
	return str_inout
	
# export triangle
def get_triangle():
	rt_list = []
	for t in mesh.tessfaces:
		if len(t.vertices) == 3:
			rt_list.append(str(t.vertices[0])+" "+str(t.vertices[1])+" "+str(t.vertices[2]))
		else:
			rt_list.append(str(t.vertices[0])+" "+str(t.vertices[1])+" "+str(t.vertices[2]))
			rt_list.append(str(t.vertices[0])+" "+str(t.vertices[2])+" "+str(t.vertices[3]))
	return rt_list

# export position
def get_position():
	rt_list = []
	for v in mesh.vertices:
		temp = str(v.co)
		temp = str_format(temp)
		rt_list.append(temp)
	return rt_list
	
# export normal
def get_normal():
	rt_list = []
	for v in mesh.vertices:
		temp = str(v.normal)
		temp = str_format(temp)
		rt_list.append(temp)
	return rt_list

# export uv
def get_uv():
	rt_list = []
	for ix in range(0, len(mesh.vertices)):
		rt_list.append("0")
	for poly in mesh.polygons:
		for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
			ix = int(mesh.loops[loop_index].vertex_index)
			temp = str(mesh.uv_layers[0].data[loop_index].uv)
			temp = str_format(temp)
			rt_list[ix] = temp
	return rt_list

#
def get_uv2():
	#
	ix_list = []
	for t in mesh.tessfaces:
		if len(t.vertices) == 3:
			ix_list.append(int(t.vertices[0]))
			ix_list.append(int(t.vertices[1]))
			ix_list.append(int(t.vertices[2]))
		else:
			ix_list.append(int(t.vertices[0]))
			ix_list.append(int(t.vertices[1]))
			ix_list.append(int(t.vertices[2]))
			ix_list.append(int(t.vertices[0]))
			ix_list.append(int(t.vertices[2]))
			ix_list.append(int(t.vertices[3]))
	#
	rt_list = []
	for ix in range(0, len(mesh.vertices)):
		rt_list.append("0")
	uv_data = mesh.tessface_uv_textures[0].data
	ix = 0
	for data in uv_data:
		if len(data.uv) == 4:
			rt_list[ix_list[ix]] = str_format(str(data.uv1))
			rt_list[ix_list[ix+1]] = str_format(str(data.uv2))
			rt_list[ix_list[ix+2]] = str_format(str(data.uv3))
			rt_list[ix_list[ix+5]] = str_format(str(data.uv4))
			ix += 6
		else:
			rt_list[ix_list[ix]] = str_format(str(data.uv1))
			rt_list[ix_list[ix+1]] = str_format(str(data.uv2))
			rt_list[ix_list[ix+2]] = str_format(str(data.uv3))
			ix +=3
	return rt_list

# export tangent
def get_tangent():
	rt_list = []
	for ix in range(0, len(mesh.vertices)):
		rt_list.append("0")
	for poly in mesh.polygons:
		for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
			ix = int(mesh.loops[loop_index].vertex_index)
			temp = str(mesh.loops[loop_index].tangent)
			temp = str_format(temp)
			temp = temp+" "+str(int(mesh.loops[loop_index].bitangent_sign))
			rt_list[ix] = temp
	return rt_list

# main check len
ex_tri = get_triangle()
ex_pos = get_position()
ex_nor = get_normal()
ex_uv = ex_tan = []
if prepare_uv():
	ex_uv = get_uv2()
	ex_tan = get_tangent()
len1 = len(ex_tri)
len2 = len(ex_pos)
len3 = len(ex_nor)
len4 = len(ex_uv)
len5 = len(ex_tan)
print("-----------------")
print("Data information:")
print("-----------------")
print("Triangle count:\t", len1)
print("Position count:\t", len2)
print("Normal count:\t", len3)
print("Uv count:\t", len4)
print("Tangent count:\t", len5)
check_len = True
if len2 != len3 or len2 != len4 or len2 != len5:
	check_len = False
	print("Export data error")

# main m3d
if check_len:
	str_out = []
	for ix in range(0, len(get_position())):
		str_out.append("Position: "+ex_pos[ix]+"\n"+"Tangent: "+ex_tan[ix]+"\n"+"Normal: "+ex_nor[ix]+"\n"+"Tex-Coords: "+ex_uv[ix]+"\n")
	export = export_dir+"export_vert.txt"
	write_text(export, str_out)
	export = export_dir+"export_tria.txt"
	write_text(export, get_triangle())
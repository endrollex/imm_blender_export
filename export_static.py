#
# export_static.py
# export static model data to text
#
import os
import bpy
os.system("cls")
mesh = bpy.data.meshes[0]

# setting export dir
export_dir = "D:\\Ashlotte\\blender\\"

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

# export triangle
def get_triangle():
	rt_list = []
	mesh.calc_tessface()
	is_ngon = False
	for t in mesh.tessfaces:
		if len(t.vertices) == 3:
			rt_list.append(str(t.vertices[0])+" "+str(t.vertices[1])+" "+str(t.vertices[2]))
		else:
			if len(t.vertices) > 4:
				is_ngon = True
			rt_list.append(str(t.vertices[0])+" "+str(t.vertices[1])+" "+str(t.vertices[2]))
			rt_list.append(str(t.vertices[0])+" "+str(t.vertices[2])+" "+str(t.vertices[3]))
	if is_ngon:
		rt_list = ["ngon detected, can not export triangle"]
	return rt_list

# export uv
def get_uv():
	try_ok = True
	uv_layer = mesh.uv_layers[0].data
	rt_list = []
	for ix in range(0, len(mesh.vertices)):
		rt_list.append("0")
	try:
		temp = mesh.uv_layers[0].data[0].uv
	except:
		try_ok = False
	if try_ok:
		for poly in mesh.polygons:
			for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
				ix = int(mesh.loops[loop_index].vertex_index)
				temp = str(uv_layer[loop_index].uv)
				temp = str_format(temp)
				rt_list[ix] = temp
	else:
		rt_list = ["no uv data"]
	return rt_list

# export tangent
def get_tangent():
	try_ok = True
	rt_list = []
	mesh.calc_tangents()
	for ix in range(0, len(mesh.vertices)):
		rt_list.append("0")
	try:
		temp = mesh.uv_layers[0].data[0].uv
	except:
		try_ok = False
	if try_ok:
		for poly in mesh.polygons:
			for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
				ix = int(mesh.loops[loop_index].vertex_index)
				temp = str(mesh.loops[loop_index].tangent)
				temp = str_format(temp)
				temp = temp+" "+str(int(mesh.loops[loop_index].bitangent_sign))
				rt_list[ix] = temp
	else:
		rt_list = ["no tangent data"]
	mesh.free_tangents()
	return rt_list

# main check len
print("-----------------")
print("Data Information:")
print("-----------------")
print("Position Count:\t", len(get_position()))
print("Normal Count:\t", len(get_normal()))
print("Triangle Count:\t", len(get_triangle()))
print("Uv Count:\t", len(get_uv()))
print("Tangent Count:\t", len(get_tangent()))

# main m3d
str_out = []
temp1 = get_position()
temp2 = get_tangent()
temp3 = get_normal()
temp4 = get_uv()
for ix in range(0, len(get_position())):
	str_out.append("Position: "+temp1[ix]+"\n"+"Tangent: "+temp2[ix]+"\n"+"Normal: "+temp3[ix]+"\n"+"Tex-Coords: "+temp4[ix]+"\n")
export = export_dir+"export_vert.txt"
write_text(export, str_out)
export = export_dir+"export_tria.txt"
write_text(export, get_triangle())
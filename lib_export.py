#
# lib_export.py
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#
import os
import bpy
os.system("cls")

# calc_tess
def calc_tess(mesh):
	if len(mesh.tessfaces) == 0:
		mesh.calc_tessface()

# find specific type index from objects
objects_mesh = []
objects_arma = []

# find_mesh, mesh which has uv
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

objects_mesh = find_mesh()
objects_arma = find_arma()
print(objects_mesh)
print(objects_arma)

for ix in objects_mesh:
	mesh = bpy.data.objects[ix].data
	print(str(ix), mesh.name, mesh.uv_textures[0].data[0].image)

#
# static_glance.py
# mesh, material and texture data structure
#
import os
import bpy
os.system("cls")

# refer
mesh = bpy.data.meshes[0]

print("-----")
print("mesh:")
print("-----")
# check tessfaces, to avoid repeated calc_tessface
if len(mesh.tessfaces) == 0:
	mesh.calc_tessface()
print("vertices:\t\t", len(mesh.vertices))
print("triangles:\t\t", "need compute")
print("vertices[0]:\t\t", mesh.vertices[0].co)
print("normal[0]:\t\t", mesh.vertices[0].normal)

# texture
print("")
print("--------")
print("texture:")
print("--------")
try:
	print("uv[0] (Tessface):\t", mesh.tessface_uv_textures[0].data[0].uv1)
	print("tangent[0]:\t\t", "need compute")
	print("diffuse map:\t\t", mesh.uv_textures[0].data[0].image.filepath)
	print("normal map:\t\t", "-")
except:
	print("texture data is not prepared")

# material
print("")
print("---------")
print("material:")
print("---------")
try:
	print("ambient:\t\t", mesh.materials[0].ambient)
	print("diffuse:\t\t", mesh.materials[0].diffuse_color)
	print("diffuse intensity:\t", mesh.materials[0].diffuse_intensity)
	print("specular:\t\t", mesh.materials[0].specular_color)
	print("specular intensity:\t", mesh.materials[0].specular_intensity)
	print("specular power:\t\t", mesh.materials[0].specular_hardness) # ShininessExponent
	print("reflect:\t\t", mesh.materials[0].mirror_color) # ReflectionColor
	print("reflect intensity:\t", mesh.materials[0].raytrace_mirror.reflect_factor)
except:
	print("material data is not prepared")
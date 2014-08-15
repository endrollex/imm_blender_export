#
# static_show.py
# Mesh, material and texture data structure
#
import os
import bpy
os.system("cls")
print("------------------------------------------")
print("Mesh, material and texture data structure:")
print("------------------------------------------")

# mesh
mesh = bpy.data.meshes[0]
print("Vertices:\t\t", len(mesh.vertices))
mesh.calc_tessface()
print("Triangles:\t\t", "Need compute")
print("Position[0]:\t\t", mesh.vertices[0].co)
print("Normal[0]:\t\t", mesh.vertices[0].normal)

# texture
try:
	print("UV[0] (Tessface):\t", mesh.tessface_uv_textures[0].data[0].uv1)
	print("Tangent[0]:\t\t", "Need compute")
	print("Diffuse map:\t\t", mesh.uv_textures[0].data[0].image.filepath)
	print("Normal map:\t\t", "-")
except:
	print("Texture data is not prepared")

# material
try:
	print("Ambient:\t\t", mesh.materials[0].ambient)
	print("Diffuse:\t\t", mesh.materials[0].diffuse_color)
	print("Diffuse intensity:\t", mesh.materials[0].diffuse_intensity)
	print("Specular:\t\t", mesh.materials[0].specular_color)
	print("Specular intensity:\t", mesh.materials[0].specular_intensity)
	print("Specular power:\t\t", mesh.materials[0].specular_hardness) # ShininessExponent
	print("Reflect:\t\t", mesh.materials[0].mirror_color) # ReflectionColor
	print("Reflect intensity:\t", mesh.materials[0].raytrace_mirror.reflect_factor)
except:
	print("Material data is not prepared")
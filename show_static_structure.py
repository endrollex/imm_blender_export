#
# show_static_structure.py
# abstract static model structure
#
import os
import bpy
os.system("cls")
print("--------------------------------")
print("Abstract static model structure:")
print("--------------------------------")

# vertices
mesh = bpy.data.meshes[0]
print("Vertex count:\t\t", len(mesh.vertices))
mesh.calc_tessface()
print("Triangle count:\t\t")
print("Index:\t\t\t", mesh.vertices[0].index)
print("Position:\t\t", mesh.vertices[0].co)
print("Normal:\t\t\t", mesh.vertices[0].normal)

# texture
try:
	print("Tex-Coords:\t\t", mesh.uv_layers[0].data[0].uv)
	mesh.calc_tangents()
	print("Tangent:\t\t", mesh.loops[0].tangent)
	print("Tangent w:\t\t", mesh.loops[0].bitangent_sign)
	mesh.free_tangents()
	print("Diffuse map:\t\t", mesh.uv_textures[0].data[0].image.filepath)
	print("Normal map:\t\t")
except:
	print("No texture data")

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
	print("No material data")
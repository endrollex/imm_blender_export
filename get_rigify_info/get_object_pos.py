#
# get_object_pos.py
#
import os
import bpy
import mathutils
import datetime
import sys
WORKING_DIR = "D:\\\EndrDocument\\ModelAnim\\imm_blender_export\\"
EXPORT_DIR = WORKING_DIR
sys.path.append(WORKING_DIR)
import imm_static
imm_static.set_global_dict("IS_LEFT_HAND", True)
os.system("cls")

def to_left_hand_vec3(vec3_in):
	return mathutils.Vector((vec3_in.x, -vec3_in.z, vec3_in.y))

# mesh
objects_mesh = imm_static.find_mesh()

# print objects
def print_objects():
	for ix in objects_mesh:
		pos = bpy.data.objects[ix].location
		pos = to_left_hand_vec3(pos)
		print(pos)

print_objects()

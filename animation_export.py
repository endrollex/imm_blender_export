#
# animation_export.py
# export animation data to text
#
import os
import copy
import bpy
import mathutils
import sys
sys.path.append("D:\\Dropbox\\imm_blender_export\\")
import static_export
os.system("cls")

# refer
o_arma = bpy.data.objects[0]
o_mesh = bpy.data.objects[2]
arma = o_arma.data
scene = bpy.data.scenes[0]
action = bpy.data.actions[0]

# get index
def get_index(item, bpy_data):
	for index, item_e in enumerate(bpy_data):
		if item_e == item:
			return index
	return -1

# data bone hierarchy
def data_hierarchy():
	rt_list = []
	for index, item in enumerate(arma.bones):
		rt_list.append([index, get_index(item.parent, arma.bones)])
	return rt_list

# data offset transformation, mesh to armature
# assume mesh's orgin is same as armature 
def data_offset():
	rt_list = []
	for ix in range(0, len(arma.bones)):
		rt_list.append(mathutils.Matrix.transposed(arma.bones[ix].matrix_local))
	return rt_list

# data time position scale rotation
def data_time_p_s_r():
	time_list = []
	pos_list = []
	sca_list = []
	rot_list = []
	#
	frame_time = 1/scene.render.fps
	cnt_bone = 0
	# time
	for bone in o_arma.pose.bones:
		time_list.append([])
		pos_list.append([])
		sca_list.append([])
		rot_list.append([])
		#
		for key in action.fcurves[0].keyframe_points:
			time_list[cnt_bone].append(key.co[0]*frame_time)
		#
		cnt_bone += 1
	# position scale rotation
	for key in action.fcurves[0].keyframe_points:
		scene.frame_set(key.co[0])
		scene.update
		for ix in range(0, cnt_bone):
			loc, rot, sca = o_arma.pose.bones[ix].matrix.decompose()
			pos_list[ix].append(loc)
			sca_list[ix].append(sca)
			rot_list[ix].append(rot)
	return [time_list, pos_list, sca_list, rot_list]

# test
print("test")
#print(data_offset())
print(data_hierarchy())
#print(data_time_p_s_r())

#
# run_script_in_blender.py
# run script in blender
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#

import sys

# WORKING_DIR: the path is the working directory.
WORKING_DIR = "D:\\x49_Documents\\Modeling_Anim\\imm_blender_export\\"
sys.path.append(WORKING_DIR)

import imm_static
import imm_anim

# EXPORT_DIR, WORKING_DIR: export directory and working directory
imm_static.set_global_dict("EXPORT_DIR", "D:\\x49_Documents\\Modeling_Anim\\m3dtob3m\\")
imm_static.set_global_dict("WORKING_DIR", WORKING_DIR)

# IS_LEFT_HARD: left hand or right hand
imm_static.set_global_dict("IS_LEFT_HAND", True)

# IS_RIGIFY: False will auto check if rigify is using, True will force to determine that model is using rigify
imm_static.set_global_dict("IS_RIGIFY", False)

# RIGIFY_GROUP_MAP: group_map file path, use ORG-Prefix bones map from DEF-Prefix bones
imm_static.set_global_dict("RIGIFY_GROUP_MAP", "rigify\\default_group_map.csv")

# RIGIFY_HIERARCHY: hierarchy file path, rebuild hierarchy
imm_static.set_global_dict("RIGIFY_HIERARCHY", "rigify\\default_hierarchy.csv")

# IS_EXPORT_ANIM: False for staic model only, True for export animation data
imm_static.set_global_dict("IS_EXPORT_ANIM", True)

# run script
imm_anim.run_script()

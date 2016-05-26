#
# run_script_in_blender.py
# run script in blender
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#

import sys

#
# the path is the working directory.
#
sys.path.append("C:\\Dropbox\\imm_blender_export\\")

import export_static
import export_anim

#
# choose a desired export function between export_static.export_m3d() and export_anim.export_m3d_anim(),
# let the other one be comment.
#
#export_static.export_m3d()
export_anim.export_m3d_anim()

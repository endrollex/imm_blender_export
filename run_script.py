#
# run_script.py
# run script
#
# Copyright 2015 Huang Yiting (http://endrollex.com)
# imm_blender_export is distributed under the terms of the GNU General Public License
#

import os
import sys
sys.path.append("C:\\Dropbox\\imm_blender_export\\")
import export_static
import export_anim
#os.system("cls")

# static
export_static.export_m3d()

# anim
#export_anim.export_m3d_anim()
imm_blender_export
==================
Python  
immature Blender export  
.m3d file format

Introduction:
-------------
* This is not a Blender addon, but a script, need to edit its settings. 
* Export Blender model data for a game engine.
* The .m3d file format is a custom file format to store meshes,
  see (Introduction to 3D Game Programming with DirectX 11 by Frank Luna).

Files Explanation:
------------------
* **imm_export.py**: Export static data to text.
* **imm_export_anim.py**: Export animation data to text.
* **global_var.py**: Global variables.

In Development:
---------------
The project is in development, maybe it can be used for export.

How to Use:
-----------
* Run the script in Blender Text Editor, and open Toggle System Console.
* Before running the script, you may edit some settings in the script files.
* This project has been tested with Blender 2.72b.

Model Data Require:
--------
* Only export meshes which has UV map.
* Armature must has only one root bone. (animation export situation)

Known Issues:
-------------
* Tangent data's algorithm sometimes will div by zero, I do not know why.
* Blender FCurve I do not understand the mechanism, in order to find all framekeys,
  simply find max framekeys in the specific FCurve.

License:
--------
* Copyright 2014 Huang Yiting (http://endrollex.com)
* imm_blender_export is distributed under the terms of the GNU General Public License
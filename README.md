imm_blender_export
==================
Python  
immature Blender export  
.m3d file format

Introduction:
-------------
* Export Blender model data for a game engine.
* The .m3d file format is a custom file format to store meshes,
  see (Introduction to 3D Game Programming with DirectX 11 by Frank Luna).

Files Explanation:
------------------
* **animation_export.py**: Export animation data to text, setting is in this file.
* **animation_glance.py**: Have a look of animation data structure.
* **static_export.py**: Export static data to text, setting is in this file.
* **static_glance.py**: Have a look of static data structure.

In Development:
---------------
The project is in development, maybe some functions can be used for export.

How to Use:
-----------
* Run the script in Blender Text Editor, and open Toggle System Console.
* Before run script, you may do some setting in the source code.

Known Issues:
-------------
* Tangent data's algorithm sometimes will div by zero, I do not know why.
* Blender FCurve I do not understand the mechanism, in order to find all framekeys,
  simply find max framekeys in the specific FCurve.

License:
--------
* Copyright 2014 Huang Yiting (http://endrollex.com)
* imm_blender_export is distributed under the terms of the GNU General Public License
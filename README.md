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
* Edit sys.path.append() in every .py file, the path is the working directory.
* Keep in Object Model.
* Only export mesh object which has UV map.
* Hide object which is not want to export.
* Exported mesh data is object's local, not world space, all world transform should be zero.
* Ensure that only one visible armature object in the scene,
  if more than one, the first visible armature will be exported. (animation export situation)
* Run the script in Blender Text Editor, and open Toggle System Console.
* This project has been tested with Blender 2.72b.

Known Issues:
-------------
* A particular step of tangent data's algorithm sometimes will div by zero, I do not know why, 
  now let this step's result to be 0.0f, it is dirty solution.
* Blender FCurve I do not understand the mechanism, in order to find all framekeys,
  simply find max framekeys in the specific FCurve.
* If you delete a bone, be sure the Vertex Group is deleted too,
  because an exported group is not according group name but the index.
* After export, You may need to manually edit the texture's name or other things.

Note:
-----
* Vertex weight will be sorted from large to small,
  sum of weight is 1.0f or 0.0f indicates 1-4 bones or none bone influences this vertex.

License:
--------
* Copyright 2014-2015 Huang Yiting (http://endrollex.com)
* imm_blender_export is distributed under the terms of the GNU General Public License
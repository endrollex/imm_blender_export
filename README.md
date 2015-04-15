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
* **export_static.py**: Export static data to text.
* **export_anim.py**: Export animation data to text.
* **global_var.py**: Global variables.
* **run_script.py**: Run script.

In Development:
---------------
The project is in development, maybe it can be used for export.

How to Use:
-----------
* Edit `sys.path.append(path)` in every python file, the path is the working directory.
  This is a little annoying.
* Hide object which is not want to export.
* Only export mesh object which has UV map.
* Exported data is object's local, not world space, all world transform should be zero and no scale.
* If have two armatrue, the first visible armature will be exported. (animation export situation)
* Keep in Object Model.
* Edit run_script.py,
  choose a export function between `export_static.export_m3d()` and `export_anim.export_m3d_anim()`,
  let the other one be comment.
* Copy and paste run_script.py to Blender Text Editor, Run Script, and open Toggle System Console.
* This project has been tested with Blender 2.74.

Known Issues:
-------------
* A particular step of tangent data's algorithm sometimes will div by zero, I do not know why,
  now let this step's result to be 0.0f, it is dirty solution.
* Blender FCurve I do not understand the mechanism, in order to find all framekeys,
  simply find max framekeys in the specific FCurve.
* After export, You may need to manually edit the texture's name or other things.

Note:
-----
* Vertex weight will be sorted from large to small,
  sum of weight is 1.0f or 0.0f indicates 1-4 bones or none bone influences this vertex.
* Rigify has 431 bones, it's too much for a game engine.
  The script use 64 ORG-Prefix bones (with a root) to rebuild hierarchy
  and redirect mesh's weight index to those bones.

License:
--------
* Copyright 2014-2015 Huang Yiting (http://endrollex.com)
* imm_blender_export is distributed under the terms of the GNU General Public License
imm_blender_export
==================
Python  
immature Blender export  
.m3d file format

Introduction:
-------------
* This is not a Blender addon, but a script, need to set up its settings. 
* Export Blender model data for a game engine.
* The .m3d file format is a custom file format to store meshes,
  see [Introduction to 3D Game Programming with DirectX 11](http://www.amazon.com/Introduction-3D-Game-Programming-DirectX/dp/1936420228/).

Files Explanation:
------------------
* **export_static.py**: Export static data to text.
* **export_anim.py**: Export animation data to text.
* **config_setup.py**: Config.
* **run_script.py**: Run script in Blender.
* **rigify\default_group_map.csv**: Redirect mesh's weight data. (Rigify situation)
* **rigify\default_hierarchy.csv**: Rebuild bone hierarchy data. (Rigify situation)

Export Limits:
--------------
* Target mesh objects must have calculated UV.
* Exported data position is object's local, not world space, all world transform should be zero and no scale.
* Only export skeletal animation data, not include physics simulation, shape keys.
* If have two armatrues, only the first visible armature will be exported.
* Armature preserve volume may be not supported, it uses dual quaternion skinning,
  however the method of Frank Luna's DX11 book is only linear blend skinning.

How to Use:
-----------
* In config_setup.py, set up `export_dir` and `working_dir`, set up more config settings if need be.
* In run_script.py, set up `sys.path.append(path)`, the path is the working directory.
  choose a desired export function between `export_static.export_m3d()` and `export_anim.export_m3d_anim()`,
  let the other one be comment.
* Hide object which is not want to export. Keep in Object Model.
* Copy and paste run_script.py to Blender Text Editor, open Toggle System Console, and Run Script.
* After exported, you must edit "Materials" part of .m3d file, and specify the diffuse/normal map name.
* This project has been tested with Blender v2.76.

Known Issues:
-------------
* A particular step of tangent data's algorithm sometimes will div by zero, I do not know why,
  now let this step's result to be 0.0f, it is dirty solution.
* Blender FCurve I do not understand the mechanism, in order to find all framekeys,
  simply find max framekeys in the specific FCurve.
* If use Rigify, please ensure ORG-Prefix bones have right pose transform.
  Rig Layers: Arm.L(Tweak), Arm.R(Tweak), Leg.L(Tweak) and Leg.R(Tweak) are not work on ORG-Prefix bones.

Note:
-----
* Vertex weight will be sorted from large to small,
  sum of weight is 1.0f or 0.0f indicates 1-4 bones or none bone influences this vertex.
* Rigify has 431 bones (Version 0.4), it's too much for a game engine.
  The script uses 64 ORG-Prefix bones and one root bone to rebuild hierarchy,
  then redirect mesh's weight index to those bones.
  If you have bones different from default rigify, edit rigify\*.csv files for adjust.

License:
--------
* Copyright 2014-2015 Huang Yiting (http://endrollex.com)
* imm_blender_export is distributed under the terms of the GNU General Public License
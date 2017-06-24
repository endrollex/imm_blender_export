imm_blender_export
==================
Python  
immature Blender export  
.m3d file format (DirectX11 Verion)

Introduction:
-------------
* This is not a Blender addon, but a script, need to setup its settings. 
* Export Blender model data for a game engine.
* The .m3d file format (DirectX11 Verion) is a custom file format to store meshes,
  see [Introduction to 3D Game Programming with DirectX 11](http://www.amazon.com/dp/1936420228/).

Files Explanation:
------------------
* **config_setup.py**: Setup configuration.
* **export_static.py**: Functions, let it be.
* **export_anim.py**: Functions, let it be.
* **run_script_in_blender.py**: Run script in Blender.
* **rigify\default_group_map.csv**: Redirect mesh's weight data. (Rigify situation)
* **rigify\default_hierarchy.csv**: Rebuild bone hierarchy data. (Rigify situation)

Export Limits:
--------------
* Target mesh objects must have calculated UV.
* Exported data position is object's local, not world space, all world transform should be zero and no scale.
* Only export skeletal animation data, not include physics, shape keys, constraints.
* If have two armatrues, only the first visible armature will be exported.
* Armature preserve volume is not supported, it uses dual quaternion skinning,
  however the method of Frank Luna's DX11 book is only linear blend skinning.

How to Use:
-----------
* In config_setup.py, setup `export_dir` and `working_dir`, setup more settings if need be.
* In run_script_in_blender.py, setup `sys.path.append(path)`, the path is the working directory.
  choose a desired export function between `export_static.export_m3d()` and `export_anim.export_m3d_anim()`,
  let the other one be comment.
* Hide objects which are not want to export. Keep in Object Model.
* Copy and paste run_script_in_blender.py to Blender Text Editor, open Toggle System Console, and Run Script.
* After exported, you must edit "Materials" part of .m3d file, and specify the diffuse/normal map name manually.
* This project has been tested with Blender v2.78.

Known Issues:
-------------
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
* The .m3d file format (DirectX12 Verion) has a bit more advanced Materials,
  see [Introduction to 3D Game Programming with DirectX 12](http://www.amazon.com/dp/1942270062).
  Notice this feature is not implemented in the script.

License:
--------
* Copyright 2014-2017 Huang Yiting (http://endrollex.com)
* imm_blender_export is distributed under the terms of the GNU General Public License
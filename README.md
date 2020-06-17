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
* **imm_static.py**: Library.
* **imm_anim.py**: Library.
* **run_script_in_blender.py**: Run this script in Blender.
* **rigify_user\default_map.csv**: Redirect mesh's weight data. (Rigify situation)
* **rigify_user\default_hierarchy.csv**: Rebuild bone hierarchy data. (Rigify situation)

Export Limits:
--------------
* Target mesh objects must have calculated UV.
* Exported data position is object's local, not world space, all world transform should be zero and no scale.
* Only export basic skeletal animation data, no advanced tech like shape keys, preserve volume.
* If have two armatrues, only the first visible armature will be exported.
* Rigify version may be varying. My work metarig is rigify 0.4.

How to Use:
-----------
* In run_script_in_blender.py, setup `WORKING_DIR` and `EXPORT_DIR`, setup more settings if need be.
* Hide objects (eye icon) which are not want to export.
* Copy and paste run_script_in_blender.py to Blender Text Editor, open Toggle System Console, and Run Script.
* After exported, you must edit "Materials" part of .m3d file, and specify the diffuse/normal map name manually.
* This project has been tested with Blender v2.82.

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
  If you have bones different from default rigify, edit rigify_custom .csv files for adjust.
* The .m3d file format (DirectX12 Verion) has a bit more advanced Materials,
  see [Introduction to 3D Game Programming with DirectX 12](http://www.amazon.com/dp/1942270062).
  Notice this feature is not implemented in the script.

License:
--------
* Copyright 2014-2017 Huang Yiting (http://endrollex.com)
* imm_blender_export is distributed under the terms of the GNU General Public License
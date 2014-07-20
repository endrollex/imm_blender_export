#
# show_static_model.py
# export static model data to text file
#
import os
import bpy
mesh = bpy.data.meshes[0]

#
export = "D:\\Ashlotte\\blender\\export_v.txt"
fw = open(export, 'w')
write_str = ""
count = 0
for v in mesh.vertices:
    temp = str(v.co)+str(v.normal)
    temp = temp.replace(")><Vector (", " ")
    temp = temp.replace("<Vector (", "")
    temp = temp.replace(",", "")
    temp = temp.replace(")>", "")
    write_str += temp+"\n"
    count += 1
write_str = str(count)+"\n"+write_str
fw.write(write_str)
fw.close()

#
mesh.calc_tessface()
export = "D:\\Ashlotte\\blender\\export_t.txt"
fw = open(export, 'w')
write_str = ""
count = 0
for t in mesh.tessfaces:
    if len(t.vertices) == 3:
        write_str += str(t.vertices[0])+" "+str(t.vertices[1])+" "+str(t.vertices[2])+"\n"
        count += 1
    else:
        write_str += str(t.vertices[0])+" "+str(t.vertices[1])+" "+str(t.vertices[2])+"\n"
        write_str += str(t.vertices[0])+" "+str(t.vertices[2])+" "+str(t.vertices[3])+"\n"
        count += 2
write_str = str(count)+"\n"+write_str
fw.write(write_str)
fw.close()
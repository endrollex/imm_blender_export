#
# export_static.py
# export static model data to text
#
import os
import bpy
mesh = bpy.data.meshes[0]

# setting export dir and files
export_dir = "D:\\Ashlotte\\blender\\"
export_f_vertices = "export_v.txt"
export_f_triangle = "export_t.txt"

# export vertices
export = export_dir+export_f_vertices
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

# export triangle
mesh.calc_tessface()
export = export_dir+export_f_triangle
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
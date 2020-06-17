# char encode:
# the value can be: utf-8, ascii, windows-1252, ...
char_encode = 'ascii'

import os
import os_base
import codecs

#
mat_data = []
ftxt = "materials_data.txt"
m3d_ex = "_export.m3d"

#
name_list = ['sinon']
name_list += ['pepper']
name_list += ['nino']
name_list += ['black_warrior']

#
mat_start = {}
mat_start['sinon'] = 0
mat_start['pepper'] = 11
mat_start['nino'] = 22
mat_start['black_warrior'] = 43

#
m3d_start = {}
m3d_start['sinon'] = 0
m3d_start['pepper'] = 0
m3d_start['nino'] = 0
m3d_start['black_warrior'] = 8

#
m3d_end = {}
m3d_end['sinon'] = 0
m3d_end['pepper'] = 0
m3d_end['nino'] = 0
m3d_end['black_warrior'] = 27


# str_replace
def str_replace(fm3d_in, mat_start_in, m3d_start_in, m3d_end_in):
	f = codecs.open(fm3d_in, encoding = char_encode)
	fw = codecs.open(fm3d_in+'t','w', encoding = char_encode)
	lines = f.readlines()
	#
	for i in range(m3d_start_in, m3d_end_in):
		lines[i] = mat_data[mat_start_in+(i-m3d_start_in)]
	for line in lines:
		fw.writelines(line)
	f.close()
	fw.close()
	#
	os.remove(fm3d_in)
	os.rename(fm3d_in+'t', fm3d_in)
	print(fm3d_in, "replace OK")

# main
assert(os.path.isfile(ftxt))
fd = codecs.open(ftxt, encoding = char_encode)
mat_data = fd.readlines()
fd.close()
for i in range(0, len(name_list)):
	fm3d = name_list[i]+m3d_ex;
	if (os.path.isfile(fm3d)):
		str_replace(fm3d, mat_start[name_list[i]], m3d_start[name_list[i]], m3d_end[name_list[i]])
print("- Program End -")
#exit = input('>')
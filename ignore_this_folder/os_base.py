#
# os_base.py
# module
# take files' path, and get all files, organize those files in a list
# Warnning: the mothod is a bad way that neglect performance
#

import os

# get files in specified directory
def get_file(cd_dir = ""):
	if (cd_dir != ""):
		cd_dir = "\\"+cd_dir
	pwd_dir = os.getcwd()+cd_dir
	list_file = os.listdir(pwd_dir)
	i_del = []
	for i, one in enumerate(list_file):
		if (cd_dir == "") and '.py' in one or os.path.isdir(pwd_dir+"\\"+one):
			i_del.append(i)
	i_offset = 0
	for i in i_del:
		del list_file[i-i_offset]
		i_offset += 1
	return list_file

# get subdir in specified directory
def get_dir(cd_dir = ""):
	if (cd_dir != ""):
		cd_dir = "\\"+cd_dir
	pwd_dir = os.getcwd()+cd_dir
	raw = os.listdir(pwd_dir)
	list_dir = []
	for ix in raw:
		if os.path.isdir(pwd_dir+"\\"+ix):
			list_dir.append(ix)
	return list_dir

# get all files
def get_all_file():
	# organize dir
	all_dir = [[""]]
	deep = -1
	no_end = True
	count = 0
	while (no_end):
		all_dir.append([]);
		deep += 1
		count = 0
		for ix0 in all_dir[deep]:
			for ix1 in get_dir(ix0):
				count += 1
				if ix1 != "":
					all_dir[deep+1].append(ix0+"\\"+ix1)
		if (count == 0): no_end = False
	all_dir.pop()
	# organize file
	all_file = [[], []]
	for i0, ix0 in enumerate(all_dir):
		for i1, ix1 in enumerate(ix0):
			for ix2 in get_file(ix1):
				all_file[0].append(ix2)
				all_file[1].append([i0, i1])
	return [all_file, all_dir]

# get file describe
def get_desc(all_file, ix):
	file_desc = [os.getcwd(), "", ""]
	file_desc[1] = all_file[1][all_file[0][1][ix][0]][all_file[0][1][ix][1]]+"\\"
	file_desc[2] = all_file[0][0][ix]
	return file_desc

# get sum
def get_sum(all_file):
	return len(all_file[0][0])

# get file full path
def get_path(all_file, ix):
	return os.getcwd()+all_file[1][all_file[0][1][ix][0]][all_file[0][1][ix][1]]+"\\"+all_file[0][0][ix]

# get file path
def get_path2(all_file, ix):
	return all_file[1][all_file[0][1][ix][0]][all_file[0][1][ix][1]]+"\\"+all_file[0][0][ix]
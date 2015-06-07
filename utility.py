import os
import errno
import tempfile
import shutil

#Gets rid of race condition and makes sure directory path exists
def make_sure_directory_exists(path):
    try:
        os.makedirs(path)
        #print('created directory: ' + path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def create_temp_directory():
	return tempfile.mkdtemp()

def delete_temp_directory(path):
	shutil.rmtree(path)


def reconstruction_possible(missing_parts):
	if len(missing_parts) < 3:
		return true
	elif len(missing_parts) > 4:
		return false
	elif missing_parts in impossible_combinations:
		return false
	else:
		return true

rec = [None] * 10
rec[0] = [[10,2,3],[9,4,5]]
rec[1] = [[10,1,3],[8,4,6]]
rec[2] = [[7,5,6],[1,2,10]]
rec[3] = [[2,8,6],[1,9,5]]
rec[4] = [[3,7,6],[1,4,9]]
rec[5] = [[3,5,7],[2,4,8]]
rec[6] = [[3,5,6]]
rec[7] = [[2,4,6]]
rec[8] = [[1,4,5]]
rec[9] = [[1,2,3]]


from zfec import filefec
from os import stat
def zfec_encode(inf, fsize, dirname, prefix, k, m, suffix='.fec', overwrite=False, verbose=False):
  with open(inf, 'rb') as f:
	  filefec.encode_to_files(f, fsize, dirname, prefix, k, m, suffix, overwrite, False)

#Remove comments to test zfec encoder with testfile
# filepath = 'test/100KB_0'
# fsize = stat(filepath).st_size
# # fsize = 1048576
# zfec_encode(filepath, fsize, 'test/', '100KB_0', 6, 10)

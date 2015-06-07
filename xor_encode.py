import Crypto.Util.strxor
from os import path, stat
from math import ceil

def sxor(s1, s2):
  s1_len = len(s1)
  s2_len = len(s2)
  if (s1_len > s2_len):
    s2 = s2.ljust(s1_len,' ')
  elif (s2_len > s1_len):
    s1 = s1.ljust(s2_len,' ')
  return Crypto.Util.strxor.strxor(s1,s2)

def encode(data):
  y7 = sxor(sxor(data[2],data[4]),data[5])
  y8 = sxor(sxor(data[1],data[3]),data[5])
  y9 = sxor(sxor(data[0],data[3]),data[4])
  y10= sxor(sxor(data[0],data[1]),data[2])
  return [y7,y8,y9,y10]

def create_part_files(part_path):
  files = [None]*10
  for i in xrange(0,10):
    files[i] = open(part_path+'.'+str(i)+'_10.partial','a')
  return files

def split_file(inf, inf_size, files):
  part_size = int(ceil(inf_size/6.0))
  # print part_size
  for i in xrange(0,6):
    part = inf.read(part_size)
    files[i].write(part)

def encode_to_files(inf, inf_size, to_path):
  data = None
  filename = path.basename(inf.name)
  part_path = path.join(to_path, filename)
  # inf_size = stat(inf).st_size
  part_size = int(ceil(inf_size/6.0))
  files = create_part_files(part_path)
  split_file(inf, inf_size, files)

  for f in xrange(0,6):
    files[f].close()
    files[f] = open(part_path+'.'+str(f)+'_10.partial','r')

  while part_size > 0:
    array = ['']*6
    for f in xrange(0,6):
      array[f] = files[f].read(4096)
    data = encode(array)
    for f in xrange(0,4):
      files[6+f].write(data[f])
    part_size -= 4096
  for f in files:
     f.close()

#Remove comment to test xor_encoder
# inf_path = 'test/100KB_0'
# with open(inf_path,'rb') as f:
#   encode_to_files(f, stat(inf_path).st_size, 'test/')
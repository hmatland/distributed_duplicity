import os
import sys
import getopt
import errno
import glob
import utility
import duplicity_conf as conf
from zfec import filefec
# import xor_encode as xor
from multiprocessing import Pool


def unwrap_self_f(arg, **kwarg):
    return Encoder.encode_file(*arg, **kwarg)

class Encoder:
  
  def __init__(self, k, n, root_source_path, target_root_path, suffix):
    self.k = k
    self.n = n
    self.root_source_path = root_source_path
    self.target_root_path = target_root_path
    self.suffix = suffix


  def encode_file(self,file_path):
    #Find the filename, used as prefix of every partial file name
    prefix = os.path.basename(file_path)
    #Find relative path from directory root to the file
    relative_path = os.path.dirname(os.path.relpath(file_path, self.root_source_path))
    #Calculate output path based on target directory path and the relative path
    output_path = os.path.join(self.target_root_path, relative_path)
    utility.make_sure_directory_exists(output_path)
    filesize = os.stat(file_path).st_size
    with open(file_path, 'rb') as f:
      filefec.encode_to_files(f, filesize, output_path, prefix, self.k, self.n, self.suffix, False, False)
      #xor.encode_to_files(f, filesize, output_path)

  def traverse_and_identify_files(self):
    file_paths = []
    for root, dirs, files in os.walk(self.root_source_path):
      for file_name in files:
        file_paths.append(os.path.join(root, file_name))
    return file_paths


  def encode_directory(self):
    utility.make_sure_directory_exists(self.target_root_path)
    files = self.traverse_and_identify_files()
    p = Pool(5)
    p.map(unwrap_self_f, zip([self]*len(files), files))
    # for f in files:
    #   self.encode_file(f)



  def move_encoded_files(self):
    for root, dirs, files in os.walk(self.target_root_path):
      relative_path = os.path.relpath(root, self.target_root_path)
      for file in files:
        from_path = os.path.join(root, file)
        for i in xrange(0,self.n):
          if (self.n>=10 and i < 10):
            tempsuffix = '0'+str(i)+'_'+str(self.n)+self.suffix
          else:
            tempsuffix = str(i)+'_'+str(self.n)+self.suffix
          # print str(i)+'_'+str(m)+suffiself.mx
          if file.endswith(str(i)+'_'+str(self.n)+self.suffix):
            to_directory = os.path.join(self.target_root_path, 'distdup'+str(i))
            to_directory = os.path.join(to_directory, relative_path)
            utility.make_sure_directory_exists(to_directory)
            to_path = os.path.join(to_directory, file)
            os.rename(from_path, to_path)
# encode_directory2('../duplicity/full2', '../split')

# zfec_encode_directory('../duplicity/full2', '../split', 7, 10, suffix='.fec', overwrite=False, verbose=False)
# move_encoded_files('../split', 10, '.fec')
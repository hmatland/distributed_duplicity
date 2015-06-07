from zfec import filefec
import os
import utility
import pprint
import zfec_decode
#import xor_decode

def decode(outfile, files, verbose=False):
  zfec_decode.decode_from_files(outfile, files, verbose)
  #xor_decode.decode_from_files(outfile, files)

class Decoder:

  def __init__(self, encoded_path, restore_path, suffix='.fec'):
    self.encoded_path = encoded_path
    self.restore_path = restore_path
    self.suffix = suffix

  def decode_directory(self):
    filedict = {}
    utility.make_sure_directory_exists(self.restore_path)

    for directory in os.listdir(self.encoded_path):
      directory_path = os.path.join(self.encoded_path, directory)
      if directory.startswith('distdup'):
        for root, dirs, files in os.walk(directory_path):
          for file in files:
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(root, directory_path)
            utility.make_sure_directory_exists(os.path.join(self.restore_path, relpath))
            filename = '.'.join(file.split('.')[:-2])
            filename = os.path.join(relpath, filename)
            if filename in filedict:
              filedict[filename].append(filepath)
            else:
              filedict[filename] = [filepath]
    for key in filedict:
      out_file_path = os.path.join(self.restore_path, key)
      partial_files_paths = filedict[key]
      decode_file_from_paths(out_file_path, partial_files_paths)


def decode_file_from_paths(output_file_path, partial_files_paths, verbose=False):
  # output_file = open(output_file_path, 'w')
  output_file = open(output_file_path, 'a')
  input_files = []
  for path in partial_files_paths:
    input_files.append(open(path, 'rb'))
  decode(output_file, input_files)
  close_files(output_file, input_files)
  return

def close_files(output_file, input_files):
  output_file.close()
  for file in input_files:
    file.close()
  return

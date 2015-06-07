import Crypto.Util.strxor
rec_equation = [None] * 10
rec_equation[0] = [[10,2,3],[9,4,5]]
rec_equation[1] = [[10,1,3],[8,4,6]]
rec_equation[2] = [[7,5,6],[1,2,10]]
rec_equation[3] = [[2,8,6],[1,9,5]]
rec_equation[4] = [[3,7,6],[1,4,9]]
rec_equation[5] = [[3,5,7],[2,4,8]]
rec_equation[6] = [[3,5,6]]
rec_equation[7] = [[2,4,6]]
rec_equation[8] = [[1,4,5]]
rec_equation[9] = [[1,2,3]]

def sxor(s1, s2):
  s1_len = len(s1)
  s2_len = len(s2)
  if s1_len > s2_len:
    s2 = s2.ljust(s1_len,' ')
  elif s2_len > s1_len:
    s1 = s1.ljust(s2_len,' ')
  return Crypto.Util.strxor.strxor(s1,s2)

def merge_files(outfile, files):
  for x in xrange(0,6):
    for f in files:
      if int(f.name[-12]) is x:
        byte = f.read(4096)
        while byte != '':
          outfile.write(byte)
          byte = f.read(4096)

def restore_partial_file(outfile, files, eq):
  req_files = []
  # print eq
  for i in eq:
    for f in files:
      if int(f.name[-12]) is (i-1):
        req_files.append(f)
  for f in req_files:
    f.seek(0,0)
  b_a = req_files[0].read(4096)
  b_b = req_files[1].read(4096)
  b_c = req_files[2].read(4096)
  while b_a != '' or b_b!='' or b_c!='':
    res = sxor(sxor(b_a, b_b),b_c)
    outfile.write(res)
    b_a = req_files[0].read(4096)
    b_b = req_files[1].read(4096)
    b_c = req_files[2].read(4096)
  for f in files:
    f.seek(0,0)

def decode_from_files(outfile,files,verbose):
  files_indices = [None]*10
  for f in files:
    files_indices[(int(f.name[-12]))] = True
  if(not None in files_indices[0:6]):
    merge_files(outfile, files)
  else:
    previousIndices = -1
    while(None in files_indices[0:6]):
      indices = [i for i, x in enumerate(files_indices) if x == None]
      if(previousIndices==indices):
        break
      # print indices
      for missing in indices:
        for eq in rec_equation[missing]:
          possible = True
          for i in eq:
            if files_indices[i-1] == None:
              possible = False
          if possible:
            filepath = list(files[0].name)
            filepath[-12] = str(missing)
            filepath = ''.join(filepath)
            with open(filepath,'w') as tempfile:
              restore_partial_file(tempfile, files, eq)
            newfile = open(filepath,'r')
            files.append(newfile)
            files_indices[missing] = True
            break
    if None in files_indices[0:6]:
      print 'Reconstruction of file :' + str(outfile.name) + ' not possible. Too few partial files available.'
    else:
      merge_files(outfile, files)

#Uncomment to test xor decoder with testfiles
# files=[]
# for x in xrange(0,10):
#   if (x != 2 and x != 3):
#       files.append(open('test/100KB_0.'+str(x)+'_10.partial'))
# with open('test/100KB_0_restore','w') as f:
#     decode_from_files(f, files, False)
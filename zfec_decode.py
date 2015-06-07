from zfec import filefec

def decode_from_files(outfile, files, verbose=False):
  filefec.decode_from_files(outfile, files, verbose)


#Remove comment to test zfec decoder with testfile
# files=[]
# for x in xrange(0,10):
#   if (x != 2 and x != 3):
#     files.append(open('test/100KB_0.0'+str(x)+'_10.fec'))
# with open('test/100KB_0_restore','a') as f:
#     decode(f, files, False)
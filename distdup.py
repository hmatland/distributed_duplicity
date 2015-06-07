import encoder
import decoder
import argparse
import os
from duplicity_distributer import Duplicity_distributer
from duplicity_restorer import Duplicity_restorer
import utility
import duplicity_conf as conf

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-k','--k', type=int, help='Number of blocks necessary to reconstruct the original data')
parser.add_argument('-n','--n', type=int, help='Total number of total blocks')
parser.add_argument('directory', help='Directory to encode or Directory to save restored backup if -r is set')
parser.add_argument('-r','--restore', action='store_true', default=False)
#parser.add_argument('target', help='Directory to store the encoded files')
args = parser.parse_args()

restore = args.restore
k= args.k
n= args.n
path = args.directory
suffix = '.fec'


if not restore:
	temp_path = utility.create_temp_directory()
	#temp_path= os.path.join(path, 'split/')
	enc = encoder.Encoder(k, n, path, temp_path, suffix)
	print ('Path to encode' + path)
	print('Path to encoded files: ' + temp_path)
	print('Number of blocks necessary to reconstruct the original data: ' + str(k))
	print('Total number of blocks: ' + str(n))
	enc.encode_directory()
	print('Moving encoded files to distdup folders')
	enc.move_encoded_files()
	print('Encoding complete')
	duplcity_distributor = Duplicity_distributer(temp_path)
	duplcity_distributor.set_up_hosts()
	duplcity_distributor.run_backup()
	duplcity_distributor.remove_env_var()
	print('Duplicity complete')
	utility.delete_temp_directory(temp_path)
else:
	restore_path = path
	temp_path = utility.create_temp_directory()
	print 'Path to encoded files: ' + temp_path
	print 'Downloading backed up files'
	duplicity_restorer = Duplicity_restorer(temp_path)
	duplicity_restorer.set_up_hosts()
	duplicity_restorer.run_restoration()
	duplicity_restorer.remove_env_var()
	print 'Decoding downloaded files'
	dec = decoder2.Decoder(temp_path, restore_path)
	dec.decode_directory()
	print 'Restored to path: '+ restore_path
	utility.delete_temp_directory(temp_path)


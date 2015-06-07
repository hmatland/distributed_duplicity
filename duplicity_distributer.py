from subprocess import call
import subprocess
import os
from multiprocessing import Pool
import duplicity_conf as conf

def execute_duplicity_command(host):
  print 'Running: '
  print host
  p = subprocess.Popen(host.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  if err:
    print 'Error while running Duplicity command: '
    print host
  print '\n'
  print 'Output from running Duplicity command: '
  print host
  print out
  print '\n'

class Duplicity_distributer:
  def __init__(self, path):
    self.path = path

  def set_up_hosts(self):
    source=os.path.join(self.path,'distdup')
    self.hosts = [None]*len(conf.remote_hosts)
    #Format every duplicity command based on configuration variables
    for i in xrange(0,len(conf.remote_hosts)):
      self.hosts[i] = 'duplicity --allow-source-mismatch {options} {source_path}{i} {host}/{remote_path}/distdup{i}'.format(source_path=source, host=conf.remote_hosts[i], remote_path=conf.remote_paths[i], options=conf.remote_host_options[i], i = i)

    #Set up any environment variables set in conf
    for env_var in conf.env_vars:
      os.environ[env_var[0]] = env_var[1]

  def run_backup(self):
    Pool().map(execute_duplicity_command, self.hosts)

  def remove_env_var(self):
    #Delete any environment variables set in conf
    for env_var in conf.env_vars:
      del os.environ[env_var[0]]

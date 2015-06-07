from subprocess import call
import subprocess
import os
from multiprocessing import Pool
import duplicity_conf as conf
import datetime

def getDateObject(hostname, remote_path, options):
  cmd = 'duplicity collection-status ' + options +' ' + hostname + '/' + remote_path
  p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  # print out.split('\n')
  if err:
    return datetime.datetime(1900,1,1)
  if 'Chain end time: ' not in out:
    return datetime.datetime(1900,1,1)
  date_object = datetime.datetime.strptime(out.split('\n')[12].replace('Chain end time: ',''),'%a %b %d %H:%M:%S %Y')
  return date_object

def execute_duplicity_command(host):
  print 'Running: '
  print host
  p = subprocess.Popen(host.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  if err:
    print 'Error while running Duplicity command: '
    print host
    print err
    return
  print '---------------------------------------'
  print 'Output from running Duplicity command: '
  print host
  print out
  print '---------------------------------------'



class Duplicity_restorer:
  def __init__(self, path):
    self.path = path

  def set_up_hosts(self):
    self.hosts = []

    #Set up any environment variables set in conf
    for env_var in conf.env_vars:
      os.environ[env_var[0]] = env_var[1]

    #Format every duplicity command based on configuration variables
    dateObjects = []
    for i in xrange(0,len(conf.remote_hosts)):
      dateObjects.append(getDateObject(conf.remote_hosts[i], conf.remote_paths[i]+'/distdup'+str(i), conf.remote_host_options[i]))
    sorted_dateObjects = sorted(dateObjects, reverse=True)
    newest_dateObject = sorted_dateObjects[0]
    max_delta = datetime.timedelta(minutes=15)
    for i in xrange(0,len(dateObjects)):
      delta = newest_dateObject-dateObjects[i]
      if max_delta > delta:
        self.hosts.append('duplicity {options} {host}/{remote_path}/distdup{i} {restore_path}/distdup{i}'.format(restore_path=self.path, host=conf.remote_hosts[i], remote_path=conf.remote_paths[i], options=conf.remote_host_options[i], i = i))
      else:
        print 'Backup of host number ' + str(i) +' is not updated or unavailable. Not downloaded.'
        print 'Corresponding command is: '
        print 'duplicity {options} {host}/{remote_path}/distdup{i} {restore_path}/distdup{i}'.format(restore_path=self.path, host=conf.remote_hosts[i], remote_path=conf.remote_paths[i], options=conf.remote_host_options[i], i = i)


  def run_restoration(self):
    Pool().map(execute_duplicity_command, self.hosts)

  def remove_env_var(self):
    #Delete any environment variables set in conf
    for env_var in conf.env_vars:
      del os.environ[env_var[0]]



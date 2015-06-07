from random import random
import argparse

parser = argparse.ArgumentParser(description='Simulate availability of distdup prototype')
parser.add_argument('-k','--k', type=int, help='Number of blocks necessary to reconstruct the original data', required=True)
parser.add_argument('-n','--n', type=int, help='Total number of total blocks', required=True)
parser.add_argument('-a','--a', type=float, help='Availability of the hosts', required=True)
parser.add_argument('-t','--trials', type=int, help='Number of trials', required=True)
args = parser.parse_args()

k= args.k
n= args.n
availability_of_hosts = args.a
trials = args.trials

def restoration_possible(backed_up_hosts, restorable_hosts, k):
  counter = 0
  for server in restorable_hosts:
    if server in backed_up_hosts:
      counter += 1
  if counter >= k:
    return True
  else:
    return False

failed_counter = 0
for i in xrange(0,trials):
  backed_up_hosts = []
  restorable_hosts = []
  for host in xrange(0,n):
    if random() < availability_of_hosts:
      backed_up_hosts.append(host)
    if random() < availability_of_hosts:
      restorable_hosts.append(host)
  if not restoration_possible(backed_up_hosts, restorable_hosts, k):
    failed_counter += 1

print 1-(float(failed_counter)/trials)


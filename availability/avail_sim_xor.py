from random import random
import argparse

parser = argparse.ArgumentParser(description='Simulate availability of distdup prototype')
parser.add_argument('-a','--a', type=float, help='Availability of the hosts', required=True)
parser.add_argument('-t','--trials', type=int, help='Number of trials', required=True)
args = parser.parse_args()

availability_of_hosts = args.a
trials = args.trials


def probability_of_restoration(backed_up_hosts, restorable_hosts):
  counter = 0
  for server in restorable_hosts:
    if server in backed_up_hosts:
      counter +=1
  if counter >= 8:
    return 1
  elif counter == 7:
    return 110.0/120
  elif counter == 6:
    return 125.0/210
  else:
    return 0
sum = 0
for i in xrange(0,trials):
  backed_up_hosts = []
  restorable_hosts = []
  for host in xrange(0,10):
    if random() < availability_of_hosts:
      backed_up_hosts.append(host)
    if random() < availability_of_hosts:
      restorable_hosts.append(host)
  sum += probability_of_restoration(backed_up_hosts, restorable_hosts)
print sum
print trials
print sum/trials

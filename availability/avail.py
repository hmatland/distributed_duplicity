from operator import mul
from fractions import Fraction
import math
import argparse

parser = argparse.ArgumentParser(description='Calculate availability of distdup prototype')
parser.add_argument('-k','--k', type=int, help='Number of blocks necessary to reconstruct the original data', default=-1)
parser.add_argument('-n','--n', type=int, help='Total number of total blocks', required=True)
parser.add_argument('-a','--a', type=float, help='Availability of the hosts, default=0.99', default=0.99)
args = parser.parse_args()

def nCk(n,k):
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

def calculate_availability(k,n, avail_hosts):
  avail_tot = 0
  for x in xrange(0,n+1):
    avail_x = 0
    for y in xrange(0,n+1):
      prob_restoration_xy = 0
      for i in xrange(0,x-k+1):
        prob_restoration_xy += nCk(n-y,i)*nCk(n-(n-y),x-i)
      prob_restoration_xy = prob_restoration_xy/float(nCk(n, x))
      avail_x += prob_restoration_xy * nCk(n,y)*(avail_hosts**y * (1-avail_hosts)**(n-y))
    avail_tot += nCk(n,x)*(avail_hosts**x)*((1-avail_hosts)**(n-x)) * avail_x
  return avail_tot

k= args.k
n= args.n
availability_of_hosts = args.a

if k == -1:
  for k in xrange(2,n):
    print 'Availability for system with optimal (' +str(n) +','+str(k) + ') erasure code scheme'
    print 'One partial part per host. Each host has availability of ' + str(availability_of_hosts)
    print calculate_availability(k,m,availability_of_hosts)
else:
  print 'Availability for system with optimal (' + str(n)+','+str(k) + ') erasure code scheme'
  print 'One partial part per host. Each host has availability of ' + str(availability_of_hosts)
  print calculate_availability(k,n,availability_of_hosts)
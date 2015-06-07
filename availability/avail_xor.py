from operator import mul
from fractions import Fraction
import math
import argparse

#Binomial coefficient
def nCk(n,k):
  return int( reduce(mul, (Fraction(n-i, i+1) for i in xrange(k)), 1) )

def probability_of_reconstruction(parts_missing):
  if parts_missing is 3:
    return 110.0/120
  elif parts_missing is 4:
    return 125.0/210
  elif parts_missing in [0,1,2]:
    return 1.0
  else:
    return 0.0

def calculate_avail_xy(x,y):
  sum = 0
  for i in xrange(0,10-max(x,y)+1):
    sum += probability_of_reconstruction(20-y-x-i)*nCk(10-y,i)*nCk(y,10-x-i)/float(nCk(10,x))
  return sum

def calculate_availability(avail_hosts):
  avail_tot = 0
  n = 10
  for x in xrange(0,11):
    avail_x = 0
    for y in xrange(0,11):
      print 'Probability in scenarion x: ' + str(x) + ' y: ' + str(y)
      avail_xy = calculate_avail_xy(x,y)
      print avail_xy
      avail_x += avail_xy * nCk(n,y)*(avail_hosts**y * (1-avail_hosts)**(n-y))
    print avail_x
    avail_tot += nCk(n,x)*(avail_hosts**x)*((1-avail_hosts)**(n-x)) * avail_x
  return avail_tot

print calculate_availability(0.99)

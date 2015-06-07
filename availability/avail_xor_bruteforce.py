import itertools
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
import math

p= [1,1,1,110.0/120,125.0/210,0,0,0,0,0,0,0,0,0,0,0,0]

def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

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

def calculate_availability(n, availability_of_host):
	hosts =[]
	for i in xrange(1,n+1):
		hosts.append(i)
	avail_total = 0
	for x in xrange(0,n+1):
		avail_x = 0
		backed_up_combinations = None
		for y in xrange(0,n+1):
			backed_up_combinations = itertools.combinations(hosts, x)
			restorable_servers_combinations = itertools.combinations(hosts,y)

			possible_counter = 0
			total_counter = 0

			for backed_up_servers in backed_up_combinations:
				for restorable_servers in restorable_servers_combinations:
					total_counter += 1
					possible_counter += probability_of_restoration(backed_up_servers,restorable_servers)
			avail_x_y = float(possible_counter)/(total_counter)
			avail_x += avail_x_y * nCk(n,y)*(availability_of_host**y * (1-availability_of_host)**(n-y))
		avail_total += nCk(n,x)*(availability_of_host**x)*((1-availability_of_host)**(n-x)) * avail_x
	return avail_total
print calculate_availability(10,0.99)
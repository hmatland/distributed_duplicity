import itertools
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
import math


def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

failure = False

def restoration_possible(backed_up_servers, restorable_servers, k):
	counter = 0
	# print backed_up_servers
	for server in restorable_servers:
		# print server
		if server in backed_up_servers:
			counter += 1
	# print counter
	if counter >= k:
		return True
	else:
		return False
def calculate_availability(k,n, availability_of_host):
	hosts =[]
	for i in xrange(1,n+1):
		hosts.append(i)
	tot_avail = 0
	for x in xrange(0,n+1):

		Availability = 0
		backed_up_combinations = None
		for y in xrange(0,n+1):

			backed_up_combinations = itertools.combinations(hosts, x)
			restorable_servers_combinations = itertools.combinations(hosts,y)

			possible_counter = 0
			total_counter = 0

			for backed_up_servers in backed_up_combinations:
				for restorable_servers in restorable_servers_combinations:

					total_counter += 1
					if restoration_possible(backed_up_servers, restorable_servers, k):
						possible_counter += 1

			percent = float(possible_counter)/(total_counter)

			Availability += percent * nCk(n,y)*(availability_of_host**y * (1-availability_of_host)**(n-y))
		tot_avail += nCk(n,x)*(availability_of_host**x)*((1-availability_of_host)**(n-x)) * Availability
	return tot_avail

for n in xrange(2,11):
	for k in xrange(1,n):
		print '\n-----------------------'
		print 'Availability for system with (' +str(n) +','+str(k) + ') erasure code scheme'
		print 'One partial part per host. Each host has availability of 0.99'
		print 'Total Avail: '+ str(calculate_availability(k,n,0.99))
print calculate_availability(3,6,0.99)
print failure
import copy
import itertools
import pprint
x1 = "01000001"
x2 = "00100100"
x3 = "00111011"
x4 = "10000001"
x5 = "11101000"
x6 = "00011101"

x = [x1,x2,x3,x4,x5,x6]
y7 = int(x3,2)^int(x5,2)^int(x6,2)
y8 = int(x2,2)^int(x4,2)^int(x6,2)
y9 = int(x1,2)^int(x4,2)^int(x5,2)
y10 = int(x1,2)^int(x2,2)^int(x3,2)

test = int(x1,2)^int(x1,2)
print '{0:b}'.format(test)

y = [int(x1,2), int(x2,2), int(x3,2), int(x4,2), int(x5,2), int(x6,2), y7, y8, y9, y10]

print y

rec_equation = [None] * 10
rec_equation[0] = [[10,2,3],[9,4,5]]
rec_equation[1] = [[10,1,3],[8,4,6]]
rec_equation[2] = [[7,5,6],[1,2,10]]
rec_equation[3] = [[2,8,6],[1,9,5]]
rec_equation[4] = [[3,7,6],[1,4,9]]
rec_equation[5] = [[3,5,7],[2,4,8]]
rec_equation[6] = [[3,5,6]]
rec_equation[7] = [[2,4,6]]
rec_equation[8] = [[1,4,5]]
rec_equation[9] = [[1,2,3]]

print y
def is_restoration_possible(dataparts):
	previousIndices = -1
	while(False in dataparts[:6]):
		indices = [i for i, x in enumerate(dataparts) if x == False]
		if(previousIndices==indices):
			break
		for missing in indices:
			for eq in rec_equation[missing]:
				possible = True
				for i in eq:
					if dataparts[i-1] == False:
						possible = False
				if possible:
					res = dataparts[eq[0]-1]^dataparts[eq[1]-1]^dataparts[eq[2]-1]
					dataparts[missing] = res
					break
		previousIndices = indices
	if False in dataparts[:6]:
		return False
	else:
		return True

hosts = [0,1,2,3,4,5,6,7,8,9]
impossible = []
for number_missing in xrange(0,5):
	combinations = itertools.combinations(hosts, number_missing)
	true_counter = 0
	false_counter = 0
	for combination in combinations:
		temp = copy.copy(y)
		# print combination
		for i in combination:
			temp[i] = False
		# print temp

		# print combination
		if(is_restoration_possible(temp)):
			true_counter += 1
		else:
			impossible.append(combination)
			# print combination
			false_counter += 1
	print '------------'
	print 'Parts missing: ' + str(number_missing)
	print true_counter
	print false_counter

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(impossible)

print len(impossible)
print (1, 6, 7) in impossible

print impossible
# print restore(y)











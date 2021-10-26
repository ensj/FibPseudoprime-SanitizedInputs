import re
import math
from datetime import datetime
from functools import reduce
from operator import mul
from datetime import datetime

# Takes a set s and returns a powerset of s.
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1, 1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

# Finds the lcm of a set of arbitrary length. 
def lcm(nums):
	if not nums:
		return 1
	if len(nums) == 1:
		return nums[0]
	return reduce(mul, nums) // reduce(math.gcd, nums)

def mem_fib(n, _cache={}):
	'''efficiently memoized recursive function, returns a Fibonacci number'''
	if n in _cache:
		return _cache[n]
	elif n > 1:
		return _cache.setdefault(n, mem_fib(n-1) + mem_fib(n-2))
	return n

def mem_lucas(n, _cache={}):
	'''efficiently memoized recursive function, returns a Lucas number'''
	if n in _cache:
		return _cache[n]
	elif n > 1:
		return _cache.setdefault(n, mem_lucas(n-1) + mem_lucas(n-2))
	elif n == 0: 
		return 2
	return n

# Fermat base-2 pseudoprime test
def b2Test(n):
	fermat = pow(2, n-1, n)
	if fermat == 1:
		print("Base-2 Fermat Pseudoprime found at: ", n)
	return [n, fermat]

# much faster base-2 pseudoprime test
def newb2Test(fibpsp, factors):
	for factor in factors:
		residue = fibpsp % (factor - 1)
		fermat = pow(2, residue, factor)
		if fermat != 2:
			return False
	return True


# processes string list of factors to int, 
# and marks if there exists a final prime factor.
def splitToMultiplicity(factors):
	normFactors = []
	for factor in factors:
		if factor.isdigit():
			normFactors.append(int(factor))
		if factor[-1] == '*':
			normFactors.append(int(factor[:-1]))

	findLast = factors[-1][0] == 'P'
	return (normFactors, findLast)

# Finds the final prime factor of a fibonacci/lucas number. 
# Refer to mersenneus for details on formatting.
def getFinalPrime(n, factors):
	nLCM = lcm(factors)
	finalPrime = n // nLCM
	if math.gcd(nLCM, finalPrime) != 1:
		finalPrime //= math.gcd(nLCM, finalPrime)
	return finalPrime

# Parses factors of Lucas numbers
def getLucas(): 
	p = re.compile(r' +')

	lucasFactors = [[-1, []] for i in range(10000)]
	lucasFactors[0] = [0, [2]]
	lucasFactors[1] = [1, []]
	with open("data/allLucasFactors.txt") as f:
		for line in f:
			rawtext = p.split(line)

			L = int(re.findall(r'\d+', rawtext[0])[0])
			factors = []

			if L % 5 == 0:
				continue

			if (len(rawtext) > 2):
				for ind in rawtext[1].strip('()').split(','):
					if ind.isdigit():
						for factor in lucasFactors[int(ind)][1]:
							if factor not in factors:
								factors.append(factor)

			splitFactors = splitToMultiplicity(rawtext[-1].strip('\n').split('.'))

			for factor in splitFactors[0]:
				factors.append(factor)

			if (splitFactors[1]):
				currLucas = mem_lucas(L)

				for i in range(len(factors)):
					factoredLuc = currLucas // factors[i]
					while (factoredLuc % factors[i] == 0):
						factoredLuc = factoredLuc // factors[i]
						factors.append(factors[i])

				finalPrime = getFinalPrime(currLucas, factors)
				if(finalPrime != 1):
					factors.append(finalPrime)
			lucasFactors[L][0] = L
			lucasFactors[L][1] = factors
	return lucasFactors

# Parses odd Fibonacci factors and constructs even Fibonnaci factors
def getFibonacci():
	p = re.compile(r' +')

	fibFactors = [[-1, []] for i in range(19999)]

	fibFactors[0] = [0, []]
	fibFactors[1] = [1, []]
	fibFactors[2] = [2, []]

	with open("data/oddFibFactors.txt") as f:
		for i, line in enumerate(f):
			L = i * 2 + 3
			factors = []

			if L % 5 == 0:
				continue

			rawtext = p.split(line)
			if (len(rawtext) > 2):
				for ind in rawtext[1].strip('()').split(','):
					for factor in fibFactors[int(ind)][1]:
						if factor not in factors:
							factors.append(factor)

			splitFactors = splitToMultiplicity(rawtext[-1].strip('\n').split('.'))
			fibn = mem_fib(L)

			for factor in splitFactors[0]:
				factors.append(factor)

			for i in range(len(factors)):
				factoredFib = fibn // factors[i]
				while (factoredFib % factors[i] == 0):
					factoredFib = factoredFib // factors[i]
					factors.append(factors[i])

			if (splitFactors[1]):
				finalPrime = getFinalPrime(mem_fib(L), factors)
				if(finalPrime != 1):
					factors.append(finalPrime)

			fibFactors[L][0] = L
			fibFactors[L][1] = factors

	lucasFactors = getLucas()

	for i in range(4, 19999, 2):
		factors = []
		L = i

		if(L % 5 == 0):
			continue

		while(L % 2 == 0):
			L //= 2
			factors += lucasFactors[L][1]
		factors += fibFactors[L][1]

		fibFactors[i][0] = i 
		fibFactors[i][1] = factors
	return fibFactors

# filters fibonacci factors into a sanitized array. 
# Refer to readme for details on how this is done.
def getSanitizedFactors():
	fibFactors = getFibonacci()

	sanitized = [[-1, [], []] for i in range(19999)]

	for L in range(19999):
		sanitized[L] = [L, list(filter(lambda x: x % L == 1, fibFactors[L][1])), list(filter(lambda x: x % L == L - 1, fibFactors[L][1]))]
	return sanitized

sanitizedFactors = getSanitizedFactors() 

# Construct & test fibonacci pseudoprimes.
length = 0
for index, [L, oneModFive, twoModFive] in enumerate(sanitizedFactors[0:], 0):
	if index%100 == 0:
		print("Progress report: Done up to L=", index, "current # of psp=",length)
	if(L == -1): 
		continue

	singletons = []
	oddMults = []
	for pset in powerset(twoModFive):
		if(len(pset) == 1):
			singletons.append(pset[0])
		elif(len(pset) % 2 == 1):
			oddMults.append(pset)

	psp = []
	for pset in powerset(oneModFive):
		oneModMult = math.prod(pset)

		for oddMult in oddMults:
			psp.append(math.prod(oddMult) * oneModMult)
			newb2Test(psp[-1], oddMult + pset)

		for single in singletons:
			psp.append(single * oneModMult)
			if(newb2Test(psp[-1], pset + [single])):
				b2Test(psp[-1])

	for oddMult in oddMults:
		psp.append(math.prod(oddMult))
		if(newb2Test(psp[-1], oddMult + pset)):
					b2Test(psp[-1])

	length += len(psp)




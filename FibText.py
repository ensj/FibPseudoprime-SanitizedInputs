import re
import math
from datetime import datetime
from functools import reduce
from operator import mul
from datetime import datetime

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1, 1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

# dumb lcm for list of arbitrary length
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

def chunks(lst, n):
	"""Yield successive n-sized chunks from lst."""
	for i in range(0, len(lst), n):
		yield lst[i:i + n]

def b2Test(n):
	fermat = pow(2, n-1, n)
	if fermat == 1:
		print("Base-2 Fermat Pseudoprime found at: ", n)
	return [n, fermat]

def newb2Test(fibpsp, factors):
	for factor in factors:
		residue = fibpsp % (factor - 1)
		fermat = pow(2, residue, factor)
		if fermat != 2:
			return False
	print("b2 pseudoprime found at", fibpsp)
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

def getFinalPrime(n, factors):
	nLCM = lcm(factors)
	finalPrime = n // nLCM
	if math.gcd(nLCM, finalPrime) != 1:
		finalPrime //= math.gcd(nLCM, finalPrime)
	return finalPrime

def getLucas(): 
	p = re.compile(r' +')

	# Handle Lucas Factors

	lucasFactors = [[-1, [], [], []] for i in range(10000)]
	lucasFactors[0] = [0, [2], [], []]
	lucasFactors[1] = [1, [], [], []]
	with open("data/allLucasFactors.txt") as f:
		for line in f:
			rawtext = p.split(line)

			L = int(re.findall(r'\d+', rawtext[0])[0])

			factors = []

			if (len(rawtext) > 2):
				for ind in rawtext[1].strip('()').split(','):
					if ind.isdigit():
						for factor in lucasFactors[int(ind)][1] + lucasFactors[int(ind)][2] + lucasFactors[int(ind)][3]:
							if factor not in factors:
								factors.append(factor)
					if ind[-1] == 'A':
						for factor in lucasFactors[int(ind[:-1])][2]:
							if factor not in factors:
								factors.append(factor)
					elif ind[-1] == 'B':
						for factor in lucasFactors[int(ind[:-1])][3]:
							if factor not in factors:
								factors.append(factor)

			splitFactors = splitToMultiplicity(rawtext[-1].strip('\n').split('.'))

			for factor in splitFactors[0]:
				factors.append(factor)

			if (splitFactors[1]):
				currLucas = -1
				if (rawtext[0][-1] == 'A'):
					currLucas = 5 * (mem_fib(L // 5) ** 2) - 5 * mem_fib(L // 5) + 1
				elif (rawtext[0][-1] == 'B'):
					currLucas = 5 * (mem_fib(L // 5) ** 2) + 5 * mem_fib(L // 5) + 1
				else: 
					currLucas = mem_lucas(L)

				finalPrime = getFinalPrime(currLucas, factors)
				if(finalPrime != 1):
					factors.append(finalPrime)

			if (rawtext[0][-1] == 'A'):
				lucasFactors[L][2] = factors
			elif (rawtext[0][-1] == 'B'):
				lucasFactors[L][3] = factors
			else:
				lucasFactors[L][0] = L
				lucasFactors[L][1] = factors
	return lucasFactors

def getFibonacci():
	p = re.compile(r' +')

	# Handle Odd Fibonacci Factors
	fibFactors = [[-1, []] for i in range(10000)]

	fibFactors[0] = [0, []]
	fibFactors[1] = [1, []]
	fibFactors[2] = [2, []]

	with open("data/oddFibFactors.txt") as f:
		for i, line in enumerate(f):
			L = i * 2 + 3
			factors = []

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

			if (splitFactors[1]):
				finalPrime = getFinalPrime(mem_fib(L), factors)
				if(finalPrime != 1):
					factors.append(finalPrime)

			fibFactors[L][0] = L
			fibFactors[L][1] = list(dict.fromkeys(factors))

	lucasFactors = getLucas()

	for i in range(4, 10000, 2):
		factors = []
		L = i
		while(L % 2 == 0):
			L //= 2
			factors += lucasFactors[L][1] + lucasFactors[L][2] + lucasFactors[L][3]
		factors += fibFactors[L][1]

		fibFactors[i][0] = i 
		fibFactors[i][1] = list(dict.fromkeys(factors))
	return fibFactors

def getSanitizedFactors():
	fibFactors = getFibonacci()

	sanitized = [[-1, [], []] for i in range(10000)]

	for L in range(10000):
		sanitized[L] = [L, list(filter(lambda x: x % L == 1, fibFactors[L][1])), list(filter(lambda x: x % L == L - 1, fibFactors[L][1]))]
	return sanitized

sanitizedFactors = getSanitizedFactors() #list(chunks(getSanitizedFactors(), 100))

#enumerate(sanitizedFactors[34:], 34) previously got to 7000
for index, [L, oneModFive, twoModFive] in enumerate(sanitizedFactors[0:], 0):
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
		pset.append(1)
		for single in singletons:
			psp.append(single * oneModMult)
			pset[-1] = single
			newb2Test(psp[-1], pset)

		pset.pop()

		for oddMult in oddMults:
			psp.append(math.prod(oddMult) * oneModMult)
			newb2Test(psp[-1], oddMult + pset)

	for oddMult in oddMults:
		psp.append(math.prod(oddMult))
		newb2Test(psp[-1], oddMult + pset)

	if index%100 == 0:
		print("Process done for L=", index)




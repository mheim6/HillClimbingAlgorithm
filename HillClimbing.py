#Artificial Intelligence 
#Monica Heim
#Assignment 2

from math import exp
from random import random,randrange,seed

index={
	"3M":1-0.0212,
	"American Express":1-0.0429,
	"Apple":1.0740,
	"Boeing":1.0468,
	"Caterpillar":1.0258,
	"Chevron":1-0.0267,
	"Cisco":1.0123,
	"Coca-Cola":1-0.0260,
	"Disney":1-0.0598,
	"Dow Chemical":1.0844,
	"Exxon Mobil":1-0.0082,
	"Goldman Sachs":1-0.0083,
	"Home Depot":1.0120,
	"IBM":1.0590,
	"Intel":1.0651,
	"Johnson & Johnson":1.0296,
	"JPMorgan Chase":1.0335,
	"McDonald's":1-0.0333,
	"Merck":1-0.0449,
	"Microsoft":1.0018,
	"Nike":1.0892,
	"Pfizer":1-0.0180,
	"Procter & Gamble":1.0032,
	"Travelers Companies Inc":1-0.0394,
	"United Technologies":1.0174,
	"UnitedHealth":1-0.0660,
	"Verizon":1.0171,
	"Visa":1-0.0353,
	"Wal-Mart":1.0146,
	"Walgreen":1.0434
}

# function: fitness - calculates current cost + gain --> sums up all earnings
# input: state
# return: return number of earnings
def fitness(s):
	f=0
	for i in s: f+=s[i]*index[i]
	return f

# function: randomstart - starts hill climbing
# input: state
# return: set of numbers n
def randomstart(s):
	val=0
	sum=0
	dist={}
	n={}
	for i in s:
		val+=s[i]
		dist[i]=randrange(100)
		sum+=dist[i]
	for i in s:
		n[i]=val*dist[i]/sum
	return n

# function: move
# input: state from a source to a destination
# return: copy of the state
def move(s,src,dst):
	n=s.copy()
	m=0.1*n[src]
	n[dst]+=m
	n[src]-=m
	return n

# function: move_rand
# input: state
# return: random move for state
def move_rand(s):
	k=list(s.keys())		# set a list of start state keys
	src=randrange(len(k))	# source
	dst=randrange(len(k))	# destination
	while dst==src: dst=randrange(len(k))
	return move(s,k[src],k[dst])

# function: move_best
# input: state s
# return: best state
def move_best(s):
	best=s.copy()			# set best state to copy of start state
	for i in s:
		for j in s:
			if i!=j:
				next=move(s,i,j)		# move the next state from start state to [i][j]
				if fitness(next)>fitness(best): best=next		# check if next earnings > best earnings, then set best to next
	return best				# return best state

# function: sch_inverse
# input: cooling schedule for simulated anneal, t = time, T = temperature
# return: time t
def sch_inverse(t):
	if t==0: return 200
	else: return 200/t-.1

# function: SA_search
# input: start state, cooling schedule
# return: current state
def SA_search(start,sch):
	cur=start.copy()		# current state set to copy of start state
	t=0						# start time t = 0 seconds

	while True:
		T=sch(t)	# temperature T = scheduled cooling at time t
		t+=1		# increment time t
		if T<=0: break			# check if temperature T greater than 1, if not then break out of loop
		next=move_rand(cur)				# make the next move be random
		dE=fitness(next)-fitness(cur)	# delta E sum of next - sum of current
		if dE>0: cur=next				# check if delta E is not negative, then sets current state to next
		else:
			p=exp(dE/T)					# probability p = e^(delta E/temperature T)
			if random()<p: cur=next		# check if a random number is less than the probability p, then set current to next
	return cur		# current state

# function: HCRR_search
# input: start state, restart limit
# return: best state
def HCRR_search(start,rlimit):
	best=start.copy()			# best state set to copy of start state
	cur=start.copy()			# current state set to copy of start state
	r=0							# restart value r start at r = 0

	while r<rlimit:
		next=move_best(cur)		# next state set to best state of the current state
		if fitness(next)>fitness(cur): cur=next		# check if next earnings greater than current earnings, then set current state to next
		else:
			if fitness(next)>fitness(best): best=next	# check if next earning greater than best earnings, then set best state to next
			cur=randomstart(cur)		# set current state to start randomly
			r+=1				# increment restart value r
	return best					# return the best state

# function: read_start
# input: (void)
# return: start state
def read_start():
	start={}
	print('\nEnter 10 Companies: ')
	for i in range(0,10):
		c=input('Company: ')
		print(c)
		if c not in index: raise IOError("Error: Not in index")
		v=float(input('  Investment: $'))
		if v<0: raise IOError("Error: Less than 0")
		start[c]=v
	return start

print("Companies:")
for i in index: print(i+", gain: %.4f"%index[i])
start=read_start()
print("\nEntered mix: %s\n  fitness: %s"%(start,fitness(start)))
sa=SA_search(start,sch_inverse)
print("\nSA mix: %s\n  fitness: %s"%(sa,fitness(sa)))
hcrr=HCRR_search(start,3)
print("\nHCRR mix: %s\n  fitness: %s"%(hcrr,fitness(hcrr)))

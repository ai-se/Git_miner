""" @Author Jchakra"""
""" This code is to run 4 different function on 4 different cores """

import multiprocessing as mp
from time import sleep


def func1():
	print("hello 1")

def func2():
	print("hello 2")

def func3():
	print("hello 3")

def func4():
	print("hello 4")

def wrapper_func(arg):
	if arg == 1:
		func1()
	if arg == 2:
		func2()
	if arg == 3:
		func3()
	if arg == 4:
		func4()

def call_yield():
	for c in range(1,5):
		yield c

if __name__ == '__main__':
	num_cpu = mp.cpu_count()
	args = list(range(num_cpu))	
	with mp.Pool(num_cpu) as p:		
		res = p.map(wrapper_func,call_yield())
		
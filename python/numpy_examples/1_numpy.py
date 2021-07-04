#!/usr/bin/env python3

import numpy as np
import time

start_time = time.time()

arr = np.array([1,2,3,4,5])
print(f"list: {arr} {time.time()-start_time}")
print(np.__version__)
print(type(arr))

arr = np.array((1,2,3,4,5))

print(f"tupele or list\narray:{arr} type{type(arr)}")

arr = np.array(43)
print(f"0 dimen array: {arr}")

arr = np.array([1,2,3,4,5])
print(f"1-D Array {arr}")

arr = np.array([[1,2,3],[4,5,6]])

print(f"2-D array {arr}")

arr = np.array([[[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]])
print("\n3-D array:An array that has 2-D arrays (matrices) as its elements is called 3-D array.")
print(arr)
print("\n")
print("Check dimensions of the array")

def check_array(ary):
	print(f"array: {ary} is of {ary.ndim} dimension\n")

a = np.array(42)
b = np.array([1,2,3,4,5])
c = np.array([[1,2,3],[4,5,6]])
d = np.array([[[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]])
check_array(a)
check_array(b)
check_array(c)
check_array(d)

arr = np.array([1,2,3,4],ndmin=5)
print(arr)
check_array(arr)

print("Python Slicing [start:end:step]\n_______________________________\n")
def slice_array(ary,s,e,stp):
	print(ary[s:e:stp])
	return ''

arr = np.array([1,2,3,4,5,6,7])

slice_array(arr,1,5,None)
slice_array(arr,4,None,None)
slice_array(arr,None,4,None)
slice_array(arr,-3,-1,None)
slice_array(arr,1,5,2)
slice_array(arr,None,None,2)

print("Slicing 2-D Arrays")
arr = np.array([[1,2,3,4,5],[6,7,8,9,10]])
print("From the second element, slice elements from index 1 to index 4 (not included)")
print(arr[1,1:4])

print("From Both elements, return index 2")
print(arr[0:2,2])

print("From both elements, slice index 1 to index 4 (not included), this will return a 2-D array:")

print(arr[0:2, 1:4])

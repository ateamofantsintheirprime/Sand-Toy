import numpy, cProfile

def zero1(array):
	for i in range(len(array)):
		array[i] = numpy.zeros((800,800))

def zero2(array):
	for i in range(len(array)):
		numpy.logical_xor(array[i], array[i], out=array[i])

print("starting")
array1 = numpy.random.randint(0, 100, size=(500, 800, 800))
print("made array1")
# array2 = numpy.random.randint(0, 100, size=(1000, 800, 800))
print("made array2")

print("starting profiling")
# cProfile.run('zero1(array1)')
# cProfile.run('zero2(array2)')
cProfile.run('numpy.logical_xor(array1,array1,out=array1)')
import sys
 
is64Bit = sys.maxsize > 2 ** 32
if is64Bit:
    print("64bit")
else:
    print("32bit")
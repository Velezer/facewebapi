from django.test import TestCase

# Create your tests here.
import time

a = 'a'
b = 'b'
start = time.time()
print(a+b)
print(time.time()-start)
start = time.time()
print(''.join([a,b]))
print(time.time()-start)
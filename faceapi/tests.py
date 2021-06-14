from django.test import TestCase

# Create your tests here.
import os
from multiprocessing import Process, Array

def square():
    for i in range(1000):
        i + i
    return 'selesai'

processes = []
num_processes = os.cpu_count()
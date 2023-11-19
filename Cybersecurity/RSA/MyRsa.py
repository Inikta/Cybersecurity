import math as m
import random

E = [3, 7, 17, 257, 65537]

def set_bit(value, bit):
    return value | (1<<bit)
def clear_bit(value, bit):
    return value & ~(1<<bit)

def montgomery_exp(x, y, R):
    

def miller_rabin_isprime(n, r):
    t = n - 1
    n2 = 0
    while (t % 2 != 1):
        odd_n /= 2
        n2 += 1
    
    for i in range(t):
        a = random.randint(2, n - 2)
        

def generate_prime(k):
    prenum = random.randint(k / 2, k - 1)
    set_bit(prenum, 0)
    set_bit(prenum, prenum.bit_length() - 1)
    set_bit(prenum, prenum.bit_length())
    
    

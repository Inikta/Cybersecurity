import math as m
import random

K_ALL = [256, 512, 1024, 2048, 4096]
E_ALL = [3, 7, 17, 257, 65537]
E = E_ALL[4]

def set_bit(value, bit):
    return value | (1<<bit)
def clear_bit(value, bit):
    return value & ~(1<<bit)

def miller_rabin_isprime(n):
    t = n - 1
    s = 0
    while (t % 2 != 1):
        t /= 2
        s += 1
    
    for i in range(10):
        a = random.randint(2, n - 2)
        x = a ^ t % n
        
        for j in range(s):
            y = x ^ 2 % n
            if ((y == 1) & (x != 1) & (x != n - 1)):
                return False
            x = y
        if (y != 1):
            return False
    
    return True
        

def generate_prime(k, occupied_number = 0):
    prenum = random.randint(k, k - 1)
    while (prenum == occupied_number):
        prenum = random.randint(k / 2, k - 1)
        
    set_bit(prenum, 0)
    set_bit(prenum, prenum.bit_length() - 1)
    set_bit(prenum, prenum.bit_length())
    
    is_prime = False
    while (not is_prime):
        is_prime = miller_rabin_isprime(prenum)
        if (not is_prime):
            prenum += 2
            
    return prenum

def xgcd(a, b):
	q = 0
	r = 1
	s1 = 1 
	s2 = 0
	s3 = 1 
	t1 = 0 
	t2 = 1
	t3 = 0
	
	while(r > 0):
		q = m.floor(a/b)
		r = a - q * b
		s3 = s1 - q * s2
		t3 = t1 - q * t2
		
		if(r > 0):
			a = b
			b = r
			s1 = s2
			s2 = s3
			t1 = t2
			t2 = t3

	return abs(b), s2, t2
    
def mod_inv(b, n):
    my_gcd, _, t = xgcd(n, b)
   
    if(my_gcd == 1):
        return t % n

def generate_keys(k_bits):
    p = generate_prime(k_bits // 2)
    while (p % E == 1):
        p = generate_prime(k_bits // 2)
    
    q = generate_prime(k_bits // 2, p)
    while (q % E == 1):
        q = generate_prime(k_bits // 2, p)
    
    N = p * q
    Phi = (p - 1) * (q - 1)
    d = mod_inv(E, Phi)
    
    return N, E, d

def encript(message : bytes, n : int, e : int):
    m = int.from_bytes(message)
    c = m ^ e % n
    return c

def decript(c : int, n : int, d : int):
    m = c ^ d % n
    return m
    
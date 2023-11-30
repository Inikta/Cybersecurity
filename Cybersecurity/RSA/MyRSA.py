import math as m
import random

K_ALL = [256, 512, 1024, 2048, 4096]
E_ALL = [3, 7, 17, 257, 65537]
E = 3 #E_ALL[0]

def set_bit(value, bit):
    return value | (1<<bit)
def clear_bit(value, bit):
    return value & ~(1<<bit)

def miller_rabin_isprime(n):        #   checked -> fine!
    t = n - 1
    s = 0
    while (t % 2 != 1):
        t //= 2
        s += 1
    
    for i in range(10):
        a = random.randint(2, n - 2)
        x = (a ** t) % n
        
        for j in range(s):
            y = (x ** 2) % n
            if ((y == 1) & (x != 1) & (x != n - 1)):
                return False
            x = y
        if (y != 1):
            return False
    
    return True

def generate_prime(k, occupied_number = 0):                     #   checked -> fine!
    prenum = random.randint((2 ** k), (2 ** (k + 1) - 1))
    while (prenum == occupied_number):
        prenum = random.randint((2 ** k), (2 ** (k + 1) - 1))
        
    prenum = set_bit(prenum, 0)
    prenum = set_bit(prenum, prenum.bit_length() - 1)
    prenum = set_bit(prenum, prenum.bit_length())
    
    is_prime = False
    while (is_prime != True):
        is_prime = miller_rabin_isprime(prenum)
        if (is_prime != True):
            #print("\tNot prime: {:d}".format(prenum))
            prenum += 2

    #print("\tPrime: {:d}".format(prenum))            
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
		q = m.floor(a / b)
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
    
def mod_inv(b, n):                  #   checked -> fine!
    my_gcd, _, t = xgcd(n, b)
   
    if (my_gcd == 1):
        return t % n

def findMinX(num, rem, k) :  
    # Compute product of all numbers  
    prod = 1
    for i in range(0, k) :  
        prod = prod * num[i]  
  
    # Initialize result  
    result = 0
  
    # Apply above formula  
    for i in range(0,k):  
        pp = prod // num[i]  
        result = result + rem[i] * mod_inv(pp, num[i]) * pp  
      
      
    return result % prod 

def generate_keys(k_bits):                  #   checked -> fine!
    p = generate_prime(k_bits // 2)
    while (p % E == 1):
        p = generate_prime(k_bits // 2)
    
    q = generate_prime(k_bits // 2, p)
    while (q % E == 1):
        q = generate_prime(k_bits // 2, p)
    
    p = 3557
    q = 2579
    
    N = p * q
    Phi = (p - 1) * (q - 1)
    d = mod_inv(E, Phi)
    
    return ((N, E), (N, d))

def encript(message, public_key):
    n = public_key[0]
    e = public_key[1]
    
    c_list = [((sym ** e) % n) for sym in message]
    return c_list

def decript(c, private_key):
    n = private_key[0]
    d = private_key[1]
    
    m_list = [((sym ** d) % n) for sym in c]
    return m_list

def sign(message):
    
    public_key, private_key = generate_keys(32)
    return encript(message, private_key), public_key

def validate(message_to_check, public_key):
    v = encript(message_to_check, public_key)
    

def main():
    public_key, private_key = generate_keys(32)
    
    message = [111111]#, 0x83, 0x65]
    print("Message: ", message)
    enc = encript(message, public_key)
    print("Encripted: ", enc)
    dec = decript(enc, private_key)
    print("Decripted: ", dec)

main()
#num = m.log2(6630165654107411377720378953380286192208449912759918282627352544091942410913058128974939606544127345462337329714291055975453672902356974158778075171192108)
#print(num)
#print(m.pow(num, 3) * 10)

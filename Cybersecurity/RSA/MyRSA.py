import math
import random

E_ALL = [3, 7, 17, 257, 65537]
E = E_ALL[0]

def set_bit(value, bit):
    return value | (1<<bit)
def clear_bit(value, bit):
    return value & ~(1<<bit)

def exponentMod(A, B, C):

    if (A == 0):
        return 0
    if (B == 0):
        return 1
    
    y = 0
    if (B % 2 == 0):
        y = exponentMod(A, B / 2, C)
        y = (y * y) % C
        
    else:
        y = A % C
        y = (y * exponentMod(A, B - 1, C) % C) % C
    return ((y + C) % C)
    
def miller_rabin_isprime(n):
    t = n - 1
    s = 0
    while (t % 2 != 1):
        t //= 2
        s += 1
    
    for i in range(10):
        a = random.randint(2, n - 2)
        x = pow(a, t, n)
        
        for j in range(s):
            y = pow(x, 2, n)
            if ((y == 1) & (x != 1) & (x != n - 1)):
                return False
            x = y
        if (y != 1):
            return False
    
    return True

def generate_prime(k, gap_size, occupied_number = 0, bit_to_change = -1):
    
    prenum = random.randint((2 ** k), (2 ** (k + 1) - 1))
    while (abs(prenum - occupied_number) <= gap_size):
        prenum = random.randint((2 ** k), (2 ** (k + 1) - 1))
        
    prenum = set_bit(prenum, 0)
    bit = bit_to_change
    if (bit == -1):
        bit = random.randint(2, 8)
        prenum = set_bit(prenum, prenum.bit_length() - bit)
    else:
        prenum = set_bit(prenum, prenum.bit_length() - bit)
    
    is_prime = False
    while (is_prime != True):
        is_prime = miller_rabin_isprime(prenum)
        if (is_prime != True):
            prenum += 2
          
    return (prenum, bit)

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
		q = a // b
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
   
    if (my_gcd == 1):
        return t % n 

def generate_keys(k_bits):
    d = None
    while (d == None):
        gap_size = 2 ** (random.randint((2 ** 13) % (k_bits // 8), (2 ** 16) % (k_bits // 4)))
        (p, bit_to_change) = generate_prime(k_bits // 2, gap_size)
        while (p % E == 1):
            (p, bit_to_change) = generate_prime(k_bits // 2, gap_size=gap_size, bit_to_change=bit_to_change)
        
        (q, bit_to_change) = generate_prime(k_bits // 2, gap_size=gap_size, occupied_number=p, bit_to_change=bit_to_change)
        while (q % E == 1):
            (q, bit_to_change) = generate_prime(k_bits // 2, gap_size=gap_size, occupied_number=p, bit_to_change=bit_to_change)

        N = p * q
        Phi = (p - 1) * (q - 1)
        d = mod_inv(E, Phi)
        
        if (d != None):
            print('> Primes generated!')
            return ((N, E), (N, d))

def create_message_digest(message : [int]):
    return message

def create_message_digest_ord(message : str):
    message_digest = [(ord(sym)) for sym in message]
    return bytes(message_digest)

def encript(message : [int], public_key):
    n = public_key[0]
    e = public_key[1]
    
    c_list = [(pow(sym, e, n)) for sym in message]
    print('> Encripted!')
    return c_list

def decript(c, private_key):
    n = private_key[0]
    d = private_key[1]

    m_list = [pow(sym, d, n) for sym in c]
    print('> Decripted!')
    return bytes(m_list)

def sign(message):
    public_key, private_key = generate_keys(32)
    message_digest = create_message_digest(message)

    signature = encript(message_digest, private_key)
    return (signature, message, public_key)

def verificate(signed):
    v1 = decript(signed[0], signed[2])
    v2 = create_message_digest(signed[1])
    
    if (v1 == v2):
        return True
    else:
        return False
    
def eratosthenes_sieve(limit):
    primes = [2]
    for i in range(3, limit + 1, 2):
        is_prime = True
        for prime in primes:
            if i % prime == 0:
                is_prime = False
                break
        if not is_prime:
            continue
        else:
            primes.append(i)

    #print("Primes: ", primes, end='\n\n')
    return primes

def main():
    public_key, private_key = generate_keys(2048)
    
    message = bytes([0x51, 0x83, 0x65])
    print("Message 1: ", message)
    enc = encript(message, public_key)
    print("Encripted 1: ", enc)
    dec = decript(enc, private_key)
    print("Decripted 1: ", dec, end='\n\n')

    message = create_message_digest_ord('[513, 0x83, 0x65]')
    print("Message 1: ", message)
    enc = encript(message, public_key)
    print("Encripted 1: ", enc)
    dec = decript(enc, private_key)
    print("Decripted 1: ", dec, end='\n\n')


    message = bytes([0x51, 0x83, 0x65])
    print("Message 1: ", message)
    signature1 = sign(message)
    print("Signature 1: ", signature1)
    res1 = verificate(signature1)
    print("Verification result 1: ", res1, end='\n\n')

    signature2 = (signature1[0], bytes([0x52, 0x83, 0x65]), signature1[2])
    print("Message 2: ", signature2[1])
    print("Signature 2: ", signature2)
    res2 = verificate(signature2)
    print("Verification result 2: ", res2, end='\n\n')

#main()

def test_rabin_miller(num, limit):
    primes = eratosthenes_sieve(limit)
    
    for prime in primes:
        if num % prime == 0:
            return prime
    
    return 1

def test():
    (p1, bit) = generate_prime(512, gap_size=256, bit_to_change=5)
    divider = test_rabin_miller(p1, 100000)
    print("Diveider for num x256: ", p1, " is ", divider)

    (p2, bit) = generate_prime(512, gap_size=512, bit_to_change=5)
    divider = test_rabin_miller(p2, 100000)
    print("Diveider for num x512: ", p2, " is ", divider)

    (p3, bit) = generate_prime(512, gap_size=1024, bit_to_change=5)
    divider = test_rabin_miller(p3, 100000)
    print("Diveider for num 1024: ", p3, " is ", divider)

    (p4, bit) = generate_prime(512, gap_size=2048, bit_to_change=5)
    divider = test_rabin_miller(p4, 1000000)
    print("Diveider for num 2048: ", p4, " is ", divider)

test()
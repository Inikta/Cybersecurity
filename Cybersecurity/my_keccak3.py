import math
import bitarray

WIDTHS = [25, 50, 100, 200, 400, 800, 1600]
b = WIDTHS[6]
w = b // 25
l = int(math.log2(w))

f = open('test.txt', 'w')

def pad(x, m):
    arr = []
    arr.append(1)
    j = 0
    if (x > 0):
        j = (-m - 2) % x

    for i in range(j):
        arr.append(0)
    arr.append(1)
    
    return arr

def xor_lists(X : bitarray.bitarray, Y : bitarray.bitarray):
    result = bitarray.bitarray(endian='little')
    for i in range(len(X)):
        result.append((X[i] ^ Y[i]))
    return result

def print_step_in_file(A : bitarray.bitarray):
    byte_str = A.tobytes()
    hex_str = byte_str.hex()
    #print(byte_str, end='\n' + str(len(byte_str)) + '\n', file=f)
    for x in range(400):
        tmp = hex_str[x]
        print(hex_str[x], end='', file=f)
        if (x == 0):
            continue
        if (x % 2 == 1):
            print('  ', end='', file=f)
        if (x % 32 == 31):
            print('\n', end='', file=f)
    print('', end='\n---------\n', file=f)

############################################

def teta(A : bitarray.bitarray):                    #checked!
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    C = bitarray.bitarray(5 * w, endian='little')
    C.setall(0)
    D = bitarray.bitarray(5 * w, endian='little')
    D.setall(0)

    for x in range(5):
        for z in range(w):
            C[w * x + z] = A[w * (5 * 0 + x) + z] 
            C[w * x + z] ^= A[w * (5 * 1 + x) + z]
            C[w * x + z] ^= A[w * (5 * 2 + x) + z]
            C[w * x + z] ^= A[w * (5 * 3 + x) + z]
            C[w * x + z] ^= A[w * (5 * 4 + x) + z]
            
    for x in range(5):
        for z in range(w):
            D[w * x + z] = C[((x-1) % 5) * w + z] 
            D[w * x + z] ^= C[((x+1) % 5) * w + ((z-1) % w)]

    for x in range(5):
        for y in range(5):
            for z in range(w):
                a[w * (5 * y + x) + z] = A[w * (5 * y + x) + z] ^ D[w * x + z]
                
    print('Teta', end='\n', file=f)
    print_step_in_file(a)
    
    return a

def ro(A : bitarray.bitarray):                      #checked!
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for z in range(w):
        a[w * (5 * 0 + 0) + z] = A[w * (5 * 0 + 0) + z]

    x = 1
    y = 0

    for t in range (24):
        for z in range(w):
            a[w * (5 * y + x) + z] = A[w * (5 * y + x) + (z - (t + 1) * (t + 2) // 2) % w]
        prev_x = x
        x = y
        y = ((2*prev_x + 3*y) % 5)
    
    print('Ro', end='\n', file=f)            
    print_step_in_file(a)
    
    return a

def pi(A : bitarray.bitarray):                      #checked!
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for x in range(5):
        for y in range(5):
            for z in range(w):
                a[w * (5 * y + x) + z] = A[w * (5 * x + ((x + 3 * y) % 5)) + z] #((x + 3 * y) % 5)
    
    print('Pi', end='\n', file=f)
    print_step_in_file(a)

    return a

def ksi(A : bitarray.bitarray):                      #checked!
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[w * (5 * y + x)+ z] = A[w * 5 * y + x * w + z] ^ ((A[w * 5 * y + ((x + 1) % 5) * w + z] ^ 1) * A[w * 5 * y + ((x + 2) % 5) * w + z])
    
    print('Ksi', end='\n', file=f)
    print_step_in_file(a)

    return a

def rc(t):
    if t % 255 == 0:
        return 1
    R = bitarray.bitarray([1, 0, 0, 0, 0, 0, 0, 0], endian='little')
    for i in range(1, t % 255 + 1):
        R.insert(0, 0)
        R[0] = R[0] ^ R[8]
        R[4] = R[4] ^ R[8]
        R[5] = R[5] ^ R[8]
        R[6] = R[6] ^ R[8]
        R = R[:8]
    return R[0]


def yota(A : bitarray.bitarray, ir):
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[w * (5 * y + x) + z] = A[w * (5 * y + x) + z]

    RC = bitarray.bitarray(w, endian='little')
    RC.setall(0)

    for j in range(l + 1):
        RC[2**j - 1] = rc(j + 7 * ir)

    for z in range(w):
        a[w * (5 * 0 + 0) + z] = a[w * (5 * 0 + 0) + z] ^ RC[z]

    print('Yota', end='\n', file=f)
    print_step_in_file(a)

    return a

def rnd_func(A : bitarray.bitarray, ir):
    result = yota(ksi(pi(ro(teta(A)))), ir)
    return result

def keccak_p(S  : bitarray.bitarray, nr):
    A = S
    print('Init', end='\n', file=f)
    print_step_in_file(A)

    for ir in range(12 + 2*l - nr, 12 + 2*l):
        print('\tRound #' + str(ir), end='\n', file=f)
        A = rnd_func(A, ir)
        print_step_in_file(A)
        
    return A

def sponge(N : bitarray.bitarray, c, d):
    r = b - c
    P = N
    P.extend(pad(r, len(N)))
    n = len(P) // r

    nr = 12 + 2*l

    P_list = [[] for i in range(n)]
    for i in range(n):
        P_list[i].extend(P[i * r : (i + 1) * r])

    S = bitarray.bitarray(1600, endian='little')
    S.setall(0)

    for i in range(n):
        P_list[i].extend(list(0 for j in range(c)))
        S = keccak_p(xor_lists(S, P_list[i]), nr)

    while (True):
        Z = S[:r]
        if (d <= len(Z)):
            a = Z[:d]
            return a
        S = keccak_p(S, nr)

def flatten(l):
    return [item for sublist in l for item in sublist]

def sha3_X(bytes_data, d):
    a = bitarray.bitarray(endian = 'little')
    a.frombytes(bytes_data)
    a.extend([0, 1])

    c = d * 2

    return sponge(a, c, d)

def shake_X(bytes_data, d):
    a = bitarray.bitarray(endian = 'little')
    a.frombytes(bytes_data)
    a.extend([1, 1, 1, 1])

    c = d * 2

    return sponge(a, c, d)

############################################

def main():
    a : bitarray.bitarray = sha3_X(b'', 256)
    print("Empty string test: ", a.tobytes().hex(), end='\n')
    print("256 Reference: \nA7 FF C6 F8 BF 1E D7 66 51 C1 47 56 A0 61 D6 62\nF5 80 FF 4D E4 3B 49 FA 82 D8 0A 4B 80 F8 43 4A", end='\n\n')
    '''
    b : bitarray.bitarray = sha3_X(bitarray.bitarray('11001', endian='big').tobytes(), 256)
    print("11001 string test: ", b.tobytes().hex(), end='\n')
    print("256 Reference: \n7B 00 47 CF 5A 45 68 82 36 3C BF 0F B0 53 22 CF\n65 F4 B7 05 9A 46 36 5E 83 01 32 E3 B5 D9 57 AF", end='\n\n')
    '''
    '''
    c : bitarray.bitarray = sha3_X(bitarray.bitarray('110010100001101011011110100110').tobytes(), 256)
    print("110010100001101011011110100110 string test: ", c.tobytes().hex(), end='\n')
    print("256 Reference: \nC8 24 2F EF 40 9E 5A E9 D1 F1 C8 57 AE 4D C6 24\nB9 2B 19 80 9F 62 AA 8C 07 41 1C 54 A0 78 B1 D0", end='\n\n')
    '''
    '''a : bitarray.bitarray = sha3_X(bitarray.bitarray('11001').tobytes(), 256)
    print("Empty string test: ", a.tobytes().hex(), end='\n')
    print("256 Reference: \nA7 FF C6 F8 BF 1E D7 66 51 C1 47 56 A0 61 D6 62 \nF5 80 FF 4D E4 3B 49 FA 82 D8 0A 4B 80 F8 43 4A", end='\n\n')
    '''
    '''big_file_w = generate_big_file('a')
    big_file_r = open('big_file_test.txt', mode='rb')
    b : bitarray.bitarray = sha3_X(big_file_r.read(), 256)
    print("Big file test: ", b.tobytes().hex(), end='\n')'''
    
def generate_big_file(rep_str):
    f = open('big_file_test.txt', mode='w', encoding='ascii')
    for i in range(1000000):
        f.write(rep_str)
    f.close()
    return f
        

main()
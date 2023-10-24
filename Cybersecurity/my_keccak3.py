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

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[w * (5 * y + x) + z] = A[w * (5 * y + x) + z] ^ D[w * x + z]
                
    print('Teta', end='\n', file=f)
    print_step_in_file(a)
    
    return a

def ro(A : bitarray.bitarray):
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

def pi(A : bitarray.bitarray):
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[w * (5 * y + x) + z] = A[5 * ((x + 3 * y) % 5) * w + x * w + z]
    
    print('Pi', end='\n', file=f)
    print_step_in_file(a)

    return a

def ksi(A : bitarray.bitarray):
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
    for i in range(1, t % 255):
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

    for j in range(l):
        RC[2**j - 1] = rc(j + 7 * ir)

    for z in range(0, w):
        a[w * (5 * 0 + 0) + z] = a[w * (5 * 0 + 0) + z] ^ RC[z]

    print('Yota', end='\n', file=f)
    print_step_in_file(a)

    return a

def rnd_func(A : bitarray.bitarray, ir):
    result = yota(ksi(pi(ro(teta(A)))), ir)
    return result

def keccak_p(S  : bitarray.bitarray, nr):
    A = S
    tmp = A.endian()
    print('Init', end='\n', file=f)
    print_step_in_file(A)

    for ir in range(12 + 2*l - nr, 12 + 2*l - 1):
        A = rnd_func(A, ir)

        print('\tRound #' + str(ir), end='\n', file=f)
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
    a : bitarray.bitarray = sha3_X(b'', 224)
    print(a.tobytes().hex())
    #print_step_in_file(a)   
    
main()
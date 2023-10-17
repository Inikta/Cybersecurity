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
    seq_len = min(len(X), len(Y))
    result = bitarray.bitarray(endian='little')
    for i in range(seq_len):
        if (X[i] == Y[i]):
            result.append(0)
        else:
            result.append(1)
    return result

def xor(x : int, y : int):
    if (x == y):
        return 0
    else:
        return 1

def create_empty_cube():
    a = [[[0 for z in range(w)] for y in range(5)] for x in range(5)]
    return a

def array_to_cube(P_list):
    A = create_empty_cube()

    for x in range(5):
        for y in range(5):
            for z in range(w):
                A[x][y][z] = P_list[x * 5 * w + y * w + z]
    return A

def cube_to_bytes_in_hex(cube):
    a = flatten(flatten(cube))
    bit_arr = bitarray.bitarray(a, endian='little')
    byte_str = bit_arr.tobytes()
    
    return byte_str.hex()

def print_step_in_file(A : bitarray.bitarray):
    byte_str = A.tobytes()
    hex_str = byte_str.hex()
    print(byte_str, end='\n' + str(len(byte_str)) + '\n', file=f)
    for x in range(24):
        for y in range(8):
            print(hex_str[x*8+y], end=' ', file=f)
        print('\n')
    print(hex_str, end='\n---------\n', file=f)

############################################

def teta(A : bitarray.bitarray):
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    C = bitarray.bitarray(5 * w, endian='little')
    C.setall(0)
    D = bitarray.bitarray(5 * w, endian='little')
    D.setall(0)

    for x in range(5):
        for z in range(w):
            C[w * x + z] = A[x * 5 * w + 0 * w + z] 
            C[w * x + z] ^= A[x * 5 * w + 1 * w + z]
            C[w * x + z] ^= A[x * 5 * w + 2 * w + z]
            C[w * x + z] ^= A[x * 5 * w + 3 * w + z]
            C[w * x + z] ^= A[x * 5 * w + 4 * w + z]
            
    for x in range(5):
        for z in range(w):
            D[w * x + z] = C[((x-1) % 5) * w + z] 
            D[w * x + z] ^= C[((x+1) % 5) * w + ((z-1) % w)]

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[x * 5 * w + y * w + z] = A[x * 5 * w + y * w + z] ^ D[w * x + z]
                
    print('Teta', end='\n', file=f)
    print_step_in_file(a)
    
    return a

def ro(A : bitarray.bitarray):
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for z in range(w):
        a[0 * 5 * w + 0 * w + z] = A[0 * 5 * w + 0 * w + z]

    x = 1
    y = 0

    for t in range (23):
        for z in range(w):
            a[x * 5 * w + y * w + z] = A[x * 5 * w + y * w + ((z - (t + 1) * (t + 2) // 2) % w)]
            tmp = x
            x = y
            y = ((2*tmp + 3*y) % 5)
    
    print('Ro', end='\n', file=f)            
    print_step_in_file(a)
    
    return a

def pi(A : bitarray.bitarray):
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[x * 5 * w + y * w + z] = A[((x + 3*y) % 5) * 5 * w + y * w + z]
    
    print('Pi', end='\n', file=f)
    print_step_in_file(a)

    return a

def ksi(A : bitarray.bitarray):
    a = bitarray.bitarray(1600, endian='little')
    a.setall(0)
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[x * 5 * w + y * w + z] = A[x * 5 * w + y * w + z] ^ ((A[((x + 1) % 5) * 5 * w + y * w + z] ^ 1) * A[((x + 2) % 5) * 5 * w + y * w + z])
    
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
                a[x * 5 * w + y * w + z] = A[x * 5 * w + y * w + z]

    RC = bitarray.bitarray(w, endian='little')
    RC.setall(0)

    for j in range(l):
        RC[2**j - 1] = rc(j + 7 * ir)

    for z in range(0, w):
        a[0 * 5 * w + 0 * w + z] = a[0 * 5 * w + 0 * w + z] ^ RC[z]

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

    for ir in range(12 + 2*l - nr, 12 + 2*l - 1):
        A = rnd_func(A, ir)

        print('\tRound #' + str(ir), end='\n', file=f)
        print_step_in_file(A)
        
    return A

def sponge(N : bitarray.bitarray, d):
    N.extend([0, 1])
    c = 2 * d
    r = b - c

    P = N
    f = len(N)
    P.extend(pad(r, len(N)))
    byteP = P.tobytes()
    hexP = byteP.hex()
    k = len(P)
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

    hex_str = bitarray.bitarray(S, endian='little').tobytes().hex()
    #Z = bitarray.bitarray(endian='little')
    while (True):
        Z = S[:r]
        if (d <= len(Z)):
            a = Z[:d]
            return a
        S = keccak_p(S, nr)

def flatten(l):
    return [item for sublist in l for item in sublist]

def keccak(bytes_data, d):
    a = bitarray.bitarray(endian = 'little')
    a.frombytes(bytes_data)
    return sponge(a, d)

############################################

def main():
    a : bitarray.bitarray = keccak(b'', 512)
    #print_step_in_file(a)   
    
main()
import math
import bitarray

WIDTHS = [25, 50, 100, 200, 400, 800, 1600]
b = WIDTHS[6]
w = b // 25
l = int(math.log2(w))

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

def xor_lists(X : list, Y : list):
    seq_len = min(len(X), len(Y))
    result = []
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
                A[x][y][z] = P_list[x * 25 + y * 5 + z]
    return A

############################################

def teta(A):
    a = create_empty_cube()
    C = [[[] for z in range(w)] for x in range(5)]
    D = [[[] for z in range(w)] for x in range(5)]

    for x in range(5):
        for z in range(w):
            C[x][z] = xor(
                xor(
                    xor(
                        xor(A[x][0][z], A[x][1][z]),
                        A[x][2][z]),
                    A[x][3][z]),
                A[x][4][z])
    for x in range(5):
        for z in range(w):
                D[x][z] = xor(C[(x-1) % 5][z], C[(x+1) % 5][(z-1) % w])

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[x][y][z] = xor(A[x][y][z], D[x][z])

    return a

def ro(A):
    a = create_empty_cube()
    for z in range(w):
        a[0][0][z] = A[0][0][z]

    (x, y) = (1, 0)

    for t in range (23):
        for z in range(w):
            a[x][y][z] = A[x][y][(z - (t + 1) * (t + 2) // 2) % w]
            x, y = y, ((2*x + 3*y) % 5)
    return a

def pi(A):
    a = create_empty_cube()
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[x][y][z] = A[(x + 3*y) % 5][x][z]
    return a

def ksi(A):
    a = create_empty_cube()
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[x][y][z] = xor(A[x][y][z],
                    (xor((A[(x + 1) % 5][y][z]), 1) * A[(x + 2) % 5][y][z]))
    return a

def rc(t):
    if t % 255 == 0:
        return 1
    R = [1, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1, t % 255):
        R.insert(0, 0)
        R[0] = xor(R[0], R[8])
        R[4] = xor(R[4], R[8])
        R[5] = xor(R[5], R[8])
        R[6] = xor(R[6], R[8])
    R = R[:8]
    return R[0]


def le(A, ir):
    a = create_empty_cube()
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                a[x][y][z] = A[x][y][z]

    RC = [0] * w

    for j in range(l):
        RC[2**j - 1] = rc(j + 7 * ir)

    for z in range(0, w):
        a[0][0][z] = xor(a[0][0][z], RC[z])

    return a

def rnd_func(A, ir):
    result = le(ksi(pi(ro(teta(A)))), ir)
    return result

def keccak_p(S, nr):
    A = array_to_cube(S)

    for ir in range(12 + 2*l - nr, 12 + 2*l - 1):
        A = rnd_func(A, ir)
    return A

def sponge(N : bitarray.bitarray, d):
    N.extend([0, 1])
    c = 2 * d
    r = b - c

    P = N
    f = len(N)
    P.extend(pad(r, len(N)))
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
        S = flatten(flatten(keccak_p(
            xor_lists(S, P_list[i]),
            nr)))

    Z = []
    while (True):
        Z.extend(S[:r])
        if (d <= len(Z)):
            a = bitarray.bitarray(Z[:d], endian = 'little')
            return a.tobytes()
        S = flatten(flatten(keccak_p(S, nr)))

def flatten(l):
    return [item for sublist in l for item in sublist]

def keccak(bytes_data, d):
    a = bitarray.bitarray(endian = 'little')
    a.frombytes(bytes_data)
    return sponge(a, d)

############################################

def main():
    a = keccak(b'', 256)
    print(a, '\n')
    #b = a.tobytes()
    #print(b, '\n')
    c = a.hex()
    print(c, '\n')
    

def test():
    a = b'abrakadabra'
    a << 1
    print(a)
main()
#test()
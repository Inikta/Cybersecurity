import bit_operations

BYTE_SIZE = 8
L = 6
W = 2 ** L

OUT_LEN = 256
FULL = 25 * W
R = 1088
C = 512

BR = R // BYTE_SIZE
BC = C // BYTE_SIZE
B_FULL = BR + BC


def complement(message, num):
    m = [message]
    ext = len(message) % B_FULL - 2
    m.append(num)
    for i in range(ext):
        m.append(0)
    m.append(num)
    return m

def absorb(block, s, n):
    b = complement(block, 0)
    hash_str = s
    for i in range(B_FULL):
        hash_str[i] = hash_str[i] ^ b[i]
    return shuffling_algorithm(hash_str, n)


def squeeze(block):
    return block[:(OUT_LEN // BYTE_SIZE)]


# ---------------
def shuffling_algorithm(block, n):
    hash = []
    for i in range(12 + 2*L - n, 12 + 2*L):
        hash.append(
            step_lya(
                step_ksi(step_pi(
                    step_ro(
                        step_teta(block)
                    )
                )), i))

def step_teta(block):
    res = []
    return res

def step_ro(block):
    res = []
    return res

def step_pi(block):
    res = []
    return res

def step_ksi(block):
    res = []
    return res

def rc(num):
    res = []
    return res

def step_lya(block, round):
    res = []
    return res
# ---------------

def entering_point(byte_data):
    chunk = complement(data_to_ints(byte_data), 1)
    n = len(chunk) // BR

    result = []
    s = bytearray(B_FULL)

    for i in range(n):
        result.append(squeeze(absorb(chunk[i * BR: (i + 1) * BR], s, n)))


def data_to_ints(data):
    int_list = []
    for sym in data:
        int_list.append(ord(sym))
    return int_list


def main():
    print("a")

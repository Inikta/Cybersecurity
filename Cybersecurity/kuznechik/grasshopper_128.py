import bitarray as ba
import math as m

BLOCK_SIZE = 16

################################################

def int_to_bitarray(num : int):
    a = ba.bitarray(endian='little')
    a.frombytes(num.to_bytes(1, 'little'))
    return a

def int_array_to_bitarrays(int_arr : [int]):
    arr = []
    for i in int_arr:
        arr.append(int_to_bitarray(i))
    return arr

def bytes_to_bitarray(intnum : int):
    a = ba.bitarray(endian='little')
    a.frombytes(intnum.to_bytes(length=1, byteorder='little'))
    return a

def byte_array_to_bitarrays(byte_arr):
    arr = []
    for i in byte_arr:
        arr.append(bytes_to_bitarray(i))
    return arr

################################################

PI = int_array_to_bitarrays(
    [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 
    46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 
    139, 1, 142, 79, 5, 132, 2, 174, 227, 106, 143, 160, 6, 11,237, 152, 127, 212, 211,31,235, 52, 44, 81, 
    234, 200, 72, 171,242, 42, 104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 
    71, 156, 183, 93, 135, 21,161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177, 50, 
    117, 25, 61,255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87, 223, 245, 36, 169, 62, 168, 67, 
    201,215, 121,214, 246, 124, 34, 185, 3, 224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 
    51, 10, 74, 167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173, 69, 70, 146, 39, 
    94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 
    136, 217, 231, 137, 225, 27, 131,73, 76, 63, 248, 254, 141,83, 170, 144, 202, 216, 133, 97, 32, 113, 
    103, 164, 45, 43, 9, 91,203, 155, 37, 208, 190, 229, 108, 82, 89, 166, 116, 210, 230, 244, 180, 192, 
    209, 102, 175, 194, 57, 75, 99, 182])

REV_PI = byte_array_to_bitarrays([
    0xA5, 0x2D, 0x32, 0x8F, 0x0E, 0x30, 0x38, 0xC0,
    0x54, 0xE6, 0x9E, 0x39, 0x55, 0x7E, 0x52, 0x91,
    0x64, 0x03, 0x57, 0x5A, 0x1C, 0x60, 0x07, 0x18,
    0x21, 0x72, 0xA8, 0xD1, 0x29, 0xC6, 0xA4, 0x3F,
    0xE0, 0x27, 0x8D, 0x0C, 0x82, 0xEA, 0xAE, 0xB4,
    0x9A, 0x63, 0x49, 0xE5, 0x42, 0xE4, 0x15, 0xB7,
    0xC8, 0x06, 0x70, 0x9D, 0x41, 0x75, 0x19, 0xC9,
    0xAA, 0xFC, 0x4D, 0xBF, 0x2A, 0x73, 0x84, 0xD5,
    0xC3, 0xAF, 0x2B, 0x86, 0xA7, 0xB1, 0xB2, 0x5B,
    0x46, 0xD3, 0x9F, 0xFD, 0xD4, 0x0F, 0x9C, 0x2F,
    0x9B, 0x43, 0xEF, 0xD9, 0x79, 0xB6, 0x53, 0x7F,
    0xC1, 0xF0, 0x23, 0xE7, 0x25, 0x5E, 0xB5, 0x1E,
    0xA2, 0xDF, 0xA6, 0xFE, 0xAC, 0x22, 0xF9, 0xE2,
    0x4A, 0xBC, 0x35, 0xCA, 0xEE, 0x78, 0x05, 0x6B,
    0x51, 0xE1, 0x59, 0xA3, 0xF2, 0x71, 0x56, 0x11,
    0x6A, 0x89, 0x94, 0x65, 0x8C, 0xBB, 0x77, 0x3C,
    0x7B, 0x28, 0xAB, 0xD2, 0x31, 0xDE, 0xC4, 0x5F,
    0xCC, 0xCF, 0x76, 0x2C, 0xB8, 0xD8, 0x2E, 0x36,
    0xDB, 0x69, 0xB3, 0x14, 0x95, 0xBE, 0x62, 0xA1,
    0x3B, 0x16, 0x66, 0xE9, 0x5C, 0x6C, 0x6D, 0xAD,
    0x37, 0x61, 0x4B, 0xB9, 0xE3, 0xBA, 0xF1, 0xA0,
    0x85, 0x83, 0xDA, 0x47, 0xC5, 0xB0, 0x33, 0xFA,
    0x96, 0x6F, 0x6E, 0xC2, 0xF6, 0x50, 0xFF, 0x5D,
    0xA9, 0x8E, 0x17, 0x1B, 0x97, 0x7D, 0xEC, 0x58,
    0xF7, 0x1F, 0xFB, 0x7C, 0x09, 0x0D, 0x7A, 0x67,
    0x45, 0x87, 0xDC, 0xE8, 0x4F, 0x1D, 0x4E, 0x04,
    0xEB, 0xF8, 0xF3, 0x3E, 0x3D, 0xBD, 0x8A, 0x88,
    0xDD, 0xCD, 0x0B, 0x13, 0x98, 0x02, 0x93, 0x80,
    0x90, 0xD0, 0x24, 0x34, 0xCB, 0xED, 0xF4, 0xCE,
    0x99, 0x10, 0x44, 0x40, 0x92, 0x3A, 0x01, 0x26,
    0x12, 0x1A, 0x48, 0x68, 0xF5, 0x81, 0x8B, 0xC7,
    0xD6, 0x20, 0x0A, 0x08, 0x00, 0x4C, 0xD7, 0x74
])

################################################

def X(a : ba.bitarray, b : ba.bitarray):
    c = ba.bitarray(8 * BLOCK_SIZE, endian='little')
    for i in range (8 * BLOCK_SIZE):
        c[i] = a[i] ^ b[i]
    return c

def S(in_data : ba.bitarray):
    res = ba.bitarray(endian='little')
    for i in range(BLOCK_SIZE):
        res.extend(PI[int.from_bytes(in_data[i * 8 : (i + 1) * 8].tobytes(), byteorder='little')])
    return res

def rev_S(in_data : ba.bitarray):
    res = ba.bitarray(endian='little')
    for i in range(BLOCK_SIZE):
        res.extend(REV_PI[int.from_bytes(in_data[i * 8 : (i + 1) * 8].tobytes(), byteorder='little')])
    return res

def GF_mul(a : ba.bitarray, b : int):
    c = ba.bitarray(8, endian='little')
    c.setall(0)
    hi_bit = ba.bitarray(endian='little')

    one = ba.bitarray(8, 'little')
    one.setall(0)
    one[7] = 1

    b_bits = ba.bitarray(endian='little')
    b_bits.frombytes(b.to_bytes(byteorder='little', length=1))

    for i in range(8):
        if (b_bits & one):
            c = c ^ a
        hi_bit = a & bytes_to_bitarray(0x80)
        a <<= 1
        if hi_bit:
            a ^= bytes_to_bitarray(0xc3)
        b_bits >>= 1
        
    return c

l_vec = [1, 148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148]

def R(state : ba.bitarray):
    vect = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    vect.setall(0)
    a_15 = ba.bitarray(8, endian='little')
    a_15.setall(0)
    for i in range(15, 0, -1):
        if (i == 15):
            vect[i * 8 :] = state[i * 8 :]
            a_15 ^= GF_mul(state[i * 8 :], l_vec[i])
        else:
            vect[(i - 1) * 8 : i * 8] = state[(i - 1) * 8 : i * 8]
            a_15 ^= GF_mul(state[(i - 1) * 8 : i * 8], l_vec[i])
    
    vect[15 * 8:] = a_15
    return vect

def rev_R(state : ba.bitarray):
    a_0 = ba.bitarray(endian='little')
    a_0 = state[15 * 8:]
    vect = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    for i in range(16):
        if (i == 15):
            vect[i * 8 :] = state[i * 8 :]
            tmp = GF_mul(vect[i * 8 :], l_vec[i])
            a_0 = a_0 ^ tmp
        else:
            vect[i * 8 : (i + 1) * 8] = state[i * 8 : (i + 1) * 8]
            tmp = GF_mul(vect[i * 8 : (i + 1) * 8], l_vec[i])
            a_0 = a_0 ^ tmp

    return vect

def L(in_data : ba.bitarray):
    vect = ba.bitarray(endian='little')
    vect = in_data[:BLOCK_SIZE * 8]
    for i in range(16):
        vect = R(vect)
    res = vect[:BLOCK_SIZE * 8]
    return res

def rev_L(in_data : ba.bitarray):
    vect = ba.bitarray(endian='little')
    vect = in_data[:BLOCK_SIZE * 8]
    for i in range(16):
        vect = rev_R(vect)
    res = vect[:BLOCK_SIZE * 8]
    return res

def prepare_iter_C():
    iter_num = []
    res = []
    for i in range(32):
        tmp = ba.bitarray(BLOCK_SIZE * 8, endian='little')
        tmp.setall(0)
        iter_num.append(tmp)
        res.append(tmp)

    for i in range(32):
        tmp2 = int_to_bitarray(i + 1)
        iter_num[i][:8] = tmp2[:8]

    for i in range(32):
        res[i] = L(iter_num[i])

    return res

def F(in_key1 : ba.bitarray, in_key2 : ba.bitarray, iter_const : ba.bitarray):
    out_key1 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    out_key2 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    vect = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    vect.setall(0)
    
    out_key2 = in_key1[:BLOCK_SIZE * 8]
    vect = X(in_key1, iter_const)
    vect = S(vect)
    vect = L(vect)
    out_key1 = X(vect, in_key2)
    
    return [out_key1, out_key2]

def expand_key(byte_key1 : bytes, byte_key2 : bytes):
    key1 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    key1.frombytes(byte_key1)

    key2 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    key2.frombytes(byte_key2)

    iter_key = []
    for i in range(32):
        tmp = ba.bitarray(BLOCK_SIZE * 8, endian='little')
        tmp.setall(0)
        iter_key.append(tmp)
    
    iter1 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    iter2 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    
    iter3 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    iter4 = ba.bitarray(BLOCK_SIZE * 8, endian='little')
    
    iter_C = prepare_iter_C()
    
    iter_key[0] = key1[:BLOCK_SIZE * 8]
    iter_key[1] = key2[:BLOCK_SIZE * 8]
    iter1 = key1[:BLOCK_SIZE * 8]
    iter2 = key2[:BLOCK_SIZE * 8]
    
    for i in range(4):
        iter3, iter4 = F(iter1, iter2, iter_C[0 + 8 * i])
        iter1, iter2 = F(iter3, iter4, iter_C[1 + 8 * i])
        iter3, iter4 = F(iter1, iter2, iter_C[2 + 8 * i])
        iter1, iter2 = F(iter3, iter4, iter_C[3 + 8 * i])
        iter3, iter4 = F(iter1, iter2, iter_C[4 + 8 * i])
        iter1, iter2 = F(iter3, iter4, iter_C[5 + 8 * i])
        iter3, iter4 = F(iter1, iter2, iter_C[6 + 8 * i])
        iter1, iter2 = F(iter3, iter4, iter_C[7 + 8 * i])
        iter_key[2 * i + 2] = iter1[:BLOCK_SIZE * 8]
        iter_key[2 * i + 3] = iter2[:BLOCK_SIZE * 8]
        
    return iter_key
    
ITER_KEY = expand_key(bytes.fromhex('8899aabbccddeeff0011223344556677'), bytes.fromhex('fedcba98765432100123456789abcdef'))

def encript_bits(blk : ba.bitarray):
    out_blk = blk[:BLOCK_SIZE * 8]
    for i in range(9):
        out_blk = X(ITER_KEY[i], out_blk)
        out_blk = S(out_blk)
        out_blk = L(out_blk)
        
    out_blk = X(out_blk, ITER_KEY[9])
    return out_blk

def decript_bits(blk : ba.bitarray):
    out_blk = blk[:BLOCK_SIZE * 8]
    out_blk = X(out_blk, ITER_KEY[9])
    for i in range(8, -1, -1):
        out_blk = rev_L(out_blk)
        out_blk = rev_S(out_blk)
        out_blk = X(out_blk, ITER_KEY[i])
        
    return out_blk

################################################

def grasshopper_encript(bytes : bytes):
    in_bits = ba.bitarray(endian='little')
    in_bits.frombytes(bytes)
    tmp1 = len(in_bits)
    out_bits = encript_bits(in_bits)
    tmp2 = len(out_bits)
    return out_bits.tobytes()

def grasshopper_decript(bytes : bytes):
    in_bits = ba.bitarray(endian='little')
    in_bits.frombytes(bytes)
    out_bits = decript_bits(in_bits)
    return out_bits.tobytes()

def main():
    
    message = b'1122334455667700ffeeddccbbaa9988'
    print("Init message: ", message, '\n')
    
    encripted = grasshopper_encript(message)
    print("Encripted: ", encripted, '\n')
    
    decripted = grasshopper_decript(encripted)
    print("Decripted: ", decripted, '\n')

main()
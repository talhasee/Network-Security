import galoisfield_inverse_gen
import binascii, copy, random, sys

# a * b modulo mx
def multiply(a, b):
    p = galoisfield_inverse_gen.mult(a, b)
    return galoisfield_inverse_gen.divide(p, int(galoisfield_inverse_gen.const, 2)).r

#x and y are 2d - number matrix of order m * n and n * p respectively.
def matrix_mult(x, y):
    m = len(x)
    n = len(x[0])
    p = len(y[0])
    q = len(y)

    ans = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            sum = 0
            for k in range(n):
                sum ^= multiply(x[i][k], y[k][j])
            ans[i][j] = sum

    return ans

def aesPolynomialMultiply(a, b):
    a = int(a, 16)
    b = int(b, 16)
    result = 0
    while b > 0:
        if b & 1 == 1:
            result = result ^ a
        a <<= 1
        if a & 0x100 == 0x100:
            a ^= 0x11B
        b >>= 1
    return hex(result)[2:].zfill(2)

def mixColumns_new(state):
    # create a new matrix to store the result
    newState = [[0 for j in range(4)] for i in range(4)]
    
    for col in range(4):
        newState[0][col] = (int(aesPolynomialMultiply('0x02',state[0][col]), 16)) ^ (int(aesPolynomialMultiply('0x03', state[1][col]), 16)) ^ (int(state[2][col], 16)) ^ (int(state[3][col], 16))
        newState[1][col] = (int(state[0][col], 16)) ^(int(aesPolynomialMultiply('0x02', state[1][col]), 16)) ^ (int(aesPolynomialMultiply('0x03', state[2][col]), 16)) ^ (int(state[3][col], 16))
        newState[2][col] = int(state[0][col], 16) ^int(state[1][col], 16) ^ int(aesPolynomialMultiply('0x02', state[2][col]), 16) ^ int(aesPolynomialMultiply('0x03', state[3][col]), 16)
        newState[3][col] = (int(aesPolynomialMultiply('0x03', state[0][col]), 16)) ^ (int(state[1][col], 16)) ^ (int(state[2][col], 16)) ^ (int(aesPolynomialMultiply('0x02', state[3][col]), 16))
    return newState
# for row in mixColumns_new([['0x87', '0xf2', '0x4d', '0x97'], ['0x6e', '0x4c', '0x90', '0xec'], ['0x46', '0xe7', '0x4a', '0xc3'], ['0xa6', '0x8c', '0xd8', '0x95']]):
#     print(row)
# for row in mixColumns_new([['0x87', '0xf2', '0x4d', '0x97'], ['0x6e', '0x4c', '0x90', '0xec'], ['0x46', '0xe7', '0x4a', '0xc3'], ['0xa6', '0x8c', '0xd8', '0x95']]):
#     print([hex(val) for val in row])
def inverse_MixColumns(state):
    gf_mul = lambda a, b: aesPolynomialMultiply(a, b)
    gf_inv = [[0x0E, 0x0B, 0x0D, 0x09],
        [0x09, 0x0E, 0x0B, 0x0D],
        [0x0D, 0x09, 0x0E, 0x0B],
        [0x0B, 0x0D, 0x09, 0x0E]
    ]
    new_state = []
    for i in range(4):
        col = []
        for j in range(4):
            s = 0
            for k in range(4):
                s ^= int(gf_mul(hex(gf_inv[i][k])[2:].zfill(2), hex(state[k][j])[2:].zfill(2)), 16)
            col.append(hex(s)[2:].zfill(2))
        new_state.append(col)
    return new_state

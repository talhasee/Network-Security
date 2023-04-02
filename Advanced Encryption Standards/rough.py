import binascii, copy, random, sys
import shift_rows
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
        # newState[0][col] = aesPolynomialMultiply('0x02', int(state[0][col], 16)) ^ aesPolynomialMultiply('0x03', int(state[1][col], 16)) ^ int(state[2][col], 16) ^ int(state[3][col], 16)
        # newState[1][col] = int(state[0][col], 16) ^ aesPolynomialMultiply('0x02', int(state[1][col], 16)) ^ aesPolynomialMultiply('0x03', int(state[2][col], 16)) ^ int(state[3][col], 16)
        # newState[2][col] = int(state[0][col], 16) ^ int(state[1][col], 16) ^ aesPolynomialMultiply('0x02', int(state[2][col], 16)) ^ aesPolynomialMultiply('0x03', int(state[3][col], 16))
        # newState[3][col] = aesPolynomialMultiply('0x03', int(state[0][col], 16)) ^ int(state[1][col], 16) ^ int(state[2][col], 16) ^ aesPolynomialMultiply('0x02', int(state[3][col], 16))
    
    return newState
# def inv_mix_columns(state):
#     gf_inv = [
#         [0x0E, 0x0B, 0x0D, 0x09],
#         [0x09, 0x0E, 0x0B, 0x0D],
#         [0x0D, 0x09, 0x0E, 0x0B],
#         [0x0B, 0x0D, 0x09, 0x0E]
#     ]
#     for i in range(4):
#         for j in range(4):
#             state[i][j] = hex(state[i][j])
#     for row in state: print(row)
#     newState = [[0 for j in range(4)] for i in range(4)]
#     for i in range(4):
#         newState[i][0] = int(aesPolynomialMultiply('0x0e', state[i][0]), 16)^int(aesPolynomialMultiply('0x09', state[i][1]), 16)^int(aesPolynomialMultiply('0x0d', state[i][2]), 16)^int(aesPolynomialMultiply('0x0b', state[i][3]), 16)
#         newState[i][1] = int(aesPolynomialMultiply('0x0b', state[i][0]), 16)^int(aesPolynomialMultiply('0x0e', state[i][1]), 16)^int(aesPolynomialMultiply('0x09', state[i][2]), 16)^int(aesPolynomialMultiply('0x0d', state[i][3]), 16)
#         newState[i][2] = int(aesPolynomialMultiply('0x0d', state[i][0]), 16)^int(aesPolynomialMultiply('0x0b', state[i][1]), 16)^int(aesPolynomialMultiply('0x0e', state[i][2]), 16)^int(aesPolynomialMultiply('0x09', state[i][3]), 16)
#         newState[i][3] = int(aesPolynomialMultiply('0x09', state[i][0]), 16)^int(aesPolynomialMultiply('0x0d', state[i][1]), 16)^int(aesPolynomialMultiply('0x0b', state[i][2]), 16)^int(aesPolynomialMultiply('0x0e', state[i][3]), 16)
#     return newState
def inv_mix_columns(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = hex(state[i][j])
    for i in range(4):
        s0 = int(aesPolynomialMultiply(str(state[i][0]), '0x0e'), 16) ^ int(aesPolynomialMultiply(str(state[i][1]), '0x0b'), 16) ^ int(aesPolynomialMultiply(str(state[i][2]), '0x0d'), 16) ^ int(aesPolynomialMultiply(str(state[i][3]), '0x09'), 16)
        s1 = int(aesPolynomialMultiply(str(state[i][0]), '0x09'), 16) ^ int(aesPolynomialMultiply(str(state[i][1]), '0x0e'), 16) ^ int(aesPolynomialMultiply(str(state[i][2]), '0x0b'), 16) ^ int(aesPolynomialMultiply(str(state[i][3]), '0x0d'), 16)
        s2 = int(aesPolynomialMultiply(str(state[i][0]), '0x0d'), 16) ^ int(aesPolynomialMultiply(str(state[i][1]), '0x09'), 16) ^ int(aesPolynomialMultiply(str(state[i][2]), '0x0e'), 16) ^ int(aesPolynomialMultiply(str(state[i][3]), '0x0b'), 16)
        s3 = int(aesPolynomialMultiply(str(state[i][0]), '0x0b'), 16) ^ int(aesPolynomialMultiply(str(state[i][1]), '0x0d'), 16) ^ int(aesPolynomialMultiply(str(state[i][2]), '0x09'), 16) ^ int(aesPolynomialMultiply(str(state[i][3]), '0x0e'), 16)
        state[i][0], state[i][1], state[i][2], state[i][3] = hex(s0)[2:].zfill(2), hex(s1)[2:].zfill(2), hex(s2)[2:].zfill(2), hex(s3)[2:].zfill(2)
    return state


def inverseMixColumns(state):
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


# state = [['0x87', '0xf2', '0x4d', '0x97'], ['0x6e', '0x4c', '0x90', '0xec'], ['0x46', '0xe7', '0x4a', '0xc3'], ['0xa6', '0x8c', '0xd8', '0x95']]
# new = mixColumns_new([['0x87', '0xf2', '0x4d', '0x97'], ['0x6e', '0x4c', '0x90', '0xec'], ['0x46', '0xe7', '0x4a', '0xc3'], ['0xa6', '0x8c', '0xd8', '0x95']])
# # for row in new:
# #     print([hex(val) for val in row])
# temp = inverseMixColumns(new)
# print()
# for row in temp:
#     print(row)
# print(aesPolynomialMultiply('0x02', '87'))
# print(int(aesPolynomialMultiply('0x02', '87'), 16))
# i = 0
# print(int(aesPolynomialMultiply('0x0e', '0x47'), 16)^int(aesPolynomialMultiply('0x09', '0x40'), 16)^int(aesPolynomialMultiply('0x0d', '0xa3'), 16)^int(aesPolynomialMultiply('0x0b', '0x4c'), 16))
# print((int(aesPolynomialMultiply('0x02',new[0][0]), 16)) ^ (int(aesPolynomialMultiply('0x03', state[1][0]), 16)) ^ (int(state[2][0], 16)) ^ (int(state[3][0], 16)))
# print(int(aesPolynomialMultiply('0x02', '87'), 16)^int(aesPolynomialMultiply('0x03', '87'), 16)^int('46', 16)^int('a6', 16))
# print(bin(int(aesPolynomialMultiply('0x02', '87'), 16)^int(aesPolynomialMultiply('0x03', '6e'), 16)^int('46', 16)^int('a6', 16)))
# print(int(aesPolynomialMultiply('0x02', '87'), 16)^int(aesPolynomialMultiply('0x03', '6e'), 16)^int('46', 16)^int('a6', 16))
# print(hex(int(aesPolynomialMultiply('0x02', '87'), 16)^int(aesPolynomialMultiply('0x03', '6e'), 16)^int('46', 16)^int('a6', 16)))
# print(bin(int(aesPolynomialMultiply('0x02', '87'), 16)))
# print(bin(int(aesPolynomialMultiply('0x03', '6e'), 16)))
# print(bin(int('46', 16)))
# print(bin(int('a6', 16)))
# print(bin(int(aesPolynomialMultiply('0x02', '87'), 16))^bin(int(aesPolynomialMultiply('0x03', '87'), 16))^bin(int('46', 16))^bin(int('a6', 16)))

#         0       1       2       3       4       5       6       7       8       9       A       B       C       D       E       F
SBOX = [['0x63', '0x7c', '0x77', '0x7b', '0xf2', '0x6b', '0x6f', '0xc5', '0x30', '0x01', '0x67', '0x2b', '0xfe', '0xd7', '0xab', '0x76'],
        ['0xca', '0x82', '0xc9', '0x7d', '0xfa', '0x59', '0x47', '0xf0', '0xad', '0xd4', '0xa2', '0xaf', '0x9c', '0xa4', '0x72', '0xc0'],
        ['0xb7', '0xfd', '0x93', '0x23', '0x36', '0x3f', '0xf7', '0xcc', '0x34', '0xa5', '0xe5', '0xf1', '0x71', '0xd8', '0x31', '0x15'], 
        ['0x04', '0xc7', '0x23', '0xc3', '0x18', '0x96', '0x05', '0x9a', '0x07', '0x12', '0x80', '0xe2', '0xeb', '0x27', '0xb2', '0x75'],
        ['0x09', '0x83', '0x2c', '0x1a', '0x1b', '0x6e', '0x5a', '0xa0', '0x52', '0x3b', '0xd6', '0xb3', '0x29', '0xe3', '0x2f', '0x84'],
        ['0x53', '0xd1', '0x00', '0xed', '0x20', '0xfc', '0xb1', '0x5b', '0x6a', '0xcb', '0xbe', '0x39', '0x4a', '0x4c', '0x58', '0xcf'],
        ['0xd0', '0xef', '0xaa', '0xfb', '0x43', '0x4d', '0x33', '0x85', '0x45', '0xf9', '0x02', '0x7f', '0x50', '0x3c', '0x9f', '0xa8'],
        ['0x51', '0xa3', '0x40', '0x8f', '0x92', '0x9d', '0x38', '0xf5', '0xbc', '0xb6', '0xda', '0x21', '0x10', '0xff', '0xf3', '0xd2'],
        ['0xcd', '0x0c', '0x13', '0xec', '0x5f', '0x97', '0x44', '0x17', '0xc4', '0xa7', '0x7e', '0x3d', '0x64', '0x5d', '0x19', '0x73'],
        ['0x60', '0x81', '0x4f', '0xdc', '0x22', '0x2a', '0x90', '0x88', '0x46', '0xee', '0xb8', '0x14', '0xde', '0x5e', '0x0b', '0xdb'], 
        ['0xe0', '0x32', '0x3a', '0x0a', '0x49', '0x06', '0x24', '0x5c', '0xc2', '0xd3', '0xac', '0x62', '0x91', '0x95', '0xe4', '0x79'],
        ['0xe7', '0xc8', '0x37', '0x6d', '0x8d', '0xd5', '0x4e', '0xa9', '0x6c', '0x56', '0xf4', '0xea', '0x65', '0x7a', '0xae', '0x08'],
        ['0xba', '0x78', '0x25', '0x2e', '0x1c', '0xa6', '0xb4', '0xc6', '0xa8', '0xdd', '0x74', '0x1f', '0x4b', '0xbd', '0x8b', '0x8a'],
        ['0x70', '0x3e', '0xb5', '0x66', '0x48', '0x03', '0xf6', '0x0e', '0x61', '0x35', '0x57', '0xb9', '0x86', '0xc1', '0x1d', '0x9e'],
        ['0xe1', '0xf8', '0x98', '0x11', '0x69', '0xd9', '0x8e', '0x94', '0x9b', '0x1e', '0x87', '0xe9', '0xce', '0x55', '0x28', '0xdf'],
        ['0x8c', '0xa1', '0x89', '0x0d', '0xbf', '0xe6', '0x42', '0x68', '0x41', '0x99', '0x2d', '0x0f', '0xb0', '0x54', '0xbb', '0x16']]

def sub_word(word):
    # Substitute each byte in the word using the S-box
    temp = [0]*len(word)
    # print(temp)
    for i in range(len(word)):
        temp[i] = hex(int(word[i], 16))
    # print(temp)
    temp[0] = SBOX[int(int(word[0])/16)][int(word[0])%16]
    temp[1] = SBOX[int(int(word[1])/16)][int(word[1])%16]
    temp[2] = SBOX[int(int(word[2])/16)][int(word[2])%16]
    temp[3] = SBOX[int(int(word[3])/16)][int(word[3])%16]
    # print(temp)
    # return [SBOX[int(byte/16)][byte%16] for byte in word]
    return temp

def rot_word(word):
    temp = shift_rows.RotateLeft(word, 1)
    return ''.join(temp)
# AES Key Expansion for 10 rounds
RCON= [
    [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
]
def key_expansion(key):
    Nk = len(key) // 4
    Nr = Nk + 6
    w = [key[i:i+4] for i in range(0, len(key), 4)]
    i = Nk
    while i < 4 * (Nr+1):
        temp = w[i-1]
        if i % Nk == 0:
            temp = sub_word(rot_word(temp))
            temp[0] = int(temp[0], 16)^RCON[0][i//Nk-1]
            print(temp)
            print(type(temp))
        elif Nk > 6 and i % Nk == 4:
            temp = sub_word(temp)
        w.append([w[i-Nk][j] ^ temp[j] for j in range(4)])
        i += 1
    return w
key = "0abcdef1234567890abcdef123456789"
# l = key_expansion(key)import pyglet
import pyglet

# Load the animation
animation = pyglet.image.load_animation('animation.gif')

# Get the dimensions of the animation
width = animation.get_max_width()
height = animation.get_max_height()

# Create a window
window = pyglet.window.Window(width=width, height=height)

# Create a sprite for the animation
sprite = pyglet.sprite.Sprite(animation)

# Set the background color to white
pyglet.gl.glClearColor(1, 1, 1, 1)

# Define the on_draw event handler
@window.event
def on_draw():
    window.clear()
    sprite.draw()

# Start the event loop
pyglet.app.run()


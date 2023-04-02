import shift_rows, sbox_generation, galoisfield_inverse_gen



# XOR function w1,w2,output = 32 bit string
def xor(w1, w2):
    w = []
    for i in range(32):
        w.append(str(int(w1[i]) ^ int(w2[i])))
    w = "".join(w)
    return w

def create_matrix_to_str(mat):
    ans = ""
    # print(type(mat[0][0]))
    for i in range(4):
        for j in range(4):
            temp = "0" + hex(mat[j][i])[2:]
            ans += temp[-2:]
    return ans



def getW(w, round):
    # print("len -- ", len(w))
    # w = [""]*44
    # w[0] = w_[0]
    # w[1] = w_[1]
    # w[2] = w_[2]
    # w[3] = w_[3]
    # print(w)
    
    for i in range(4, 41, 4):
        w.append(xor(gBox(w[i - 1], i // 4), w[i - 4]))
        w.append(xor(w[i], w[i - 3]))
        w.append(xor(w[i + 1], w[i - 2]))
        w.append(xor(w[i + 2], w[i - 1]))
        # w[i] = xor(gBox(w[i - 1], i // 4), w[i - 4])
        # w[i + 1] = xor(w[i], w[i - 3])
        # w[i + 2] = xor(w[i + 1], w[i - 2])
        # w[i + 3] = xor(w[i + 2], w[i - 1])
    # i = 0
    # w[i] = xor(gBox(w[3], round), w[0])
    # w[i + 1] = xor(w[i], w[i+1])
    # w[i + 2] = xor(w[i + 1], w[i + 2])
    # w[i + 3] = xor(w[i + 2], w[i + 3])
    return w

def create_str_to_bin_matrix(x):
    ans = []
    for i in range(4):
        ans.append([])
    for i in range(4):
        for j in range(4):
            ans[i].append(x[j * 32 + i * 8:j * 32 + i * 8 + 8])
    return ans

# Key matrix for a given round  Input = 128 bit hex string Output = 4 * 4 byte matrix(Number)
def aes_keymat(key, round):
    

    # w = [w0,w1,w2,w3] wi = 32 bit binary string output = 4 * 4 byte(Number) matrix.
    def create_w_to_mat(w):
        ans = []
        for i in range(4):
            ans.append([])
            for j in range(4):
                ans[i].append(int(w[j][8 * i:8 * i + 8], 2))
        return ans

    # byte(string) matrix to w0, w1 ,w2 ,w3 - bytes(string)
    def create_mat_to_w(mat):
        w = []
        for i in range(4):
            w.append("")
            for j in range(4):
                w[i] += mat[j][i]
        return w


    key = create_hex_to_bin_str(key, len(key))
    # print(key)
    matrix = create_str_to_bin_matrix(key)  # 4 * 4 byte(string) array
    # for row in matrix:
    #     print(row)
    # print("Round - ", round)
    w = create_mat_to_w(matrix)  # w is 32 bits string array.
    # print(w)
    w = getW(w, round)
    # t = w
    # print(w)
    w = [w[0 + 4 * round], w[1 + 4 * round], w[2 + 4 * round], w[3 + 4 * round]]
    # print("w -- ", w, " ", t == w)
    return create_w_to_mat(w)

def gBox(w, round):
    def stringToByte(w):
        temp = []
        # print("Here..", w)
        for i in range(4):
            temp.append(w[i * 8:(i + 1) * 8])
        temp = list(map(lambda x: int(x, 2), temp))
        return temp

    w = stringToByte(w)
    w = shift_rows.RotateLeft(w, 1)
    for i in range(4):
        w[i] = sbox_generation.sbox(hex(w[i])[2:])
    w = list(map(lambda x: int(x, 16), w))
    temp = rc(round)
    # temp2 = (int)temp
    # print(type(temp))
    w[0] = w[0] ^ rc(round)
    # w[0] = w[0] ^ temp2
    w = list(map(lambda x: ("00000000" + bin(x)[2:])[-8:], w))
    return ''.join(w)

def rc(j):
    Dict = galoisfield_inverse_gen.divide(2**(j-1), int(galoisfield_inverse_gen.const, 2))
    temp = Dict['r']
    return (int)(temp)

def create_hex_to_bin_str(hex_str, n):
    def create_hex_to_str(h):
        byteString = "0000" + bin(int(h, 16))[2:]
        return byteString[-4:]

    prefix = "0" * n
    str_ = prefix + hex_str
    str_ = str_[-n:]

    ans = ""
    for char in str_:
        ans += create_hex_to_str(char)

    return ans




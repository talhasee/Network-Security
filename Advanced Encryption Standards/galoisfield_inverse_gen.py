const = "100011011" #Assuming its a constant

def mult(x, y):
    a = bin(x)[2:]
    b = bin(y)[2:]
    ans = 0
    for i in range(len(b)):
        if b[i] == '1':
            ans ^= int(a, 2)
        if i != len(b) - 1:
            ans <<= 1
    return ans


def divide(a, b):
    q = ['0'] * 10
    # print(a, " ", b)

    def find_degree(x):
        # print(type(x))
        return len(bin(int(x))[2:]) - 1


    if find_degree(a) < find_degree(b):
        return {'r': a, 'q': 0}
    while find_degree(a) >= find_degree(b):
        count = 0
        d = b
        while find_degree(d) < find_degree(a):
            d = d << 1
            count += 1
        r = d ^ a
        # print(count)
        q[count] = '1'
        if r == 0 or find_degree(r) < find_degree(b):
            return {'r': r, 'q': int(''.join(q[::-1]), 2)}
        a = r
    return None


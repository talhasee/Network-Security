def RotateRight(arr, i):
    ans = [0] * len(arr)
    for j in range(len(arr)):
        ans[(j+i) % len(arr)] = arr[j]
    return ans

def RotateLeft(arr, i):
    ans = [0] * len(arr)
    for j in range(len(arr)):
        ans[(j-i+len(arr)) % len(arr)] = arr[j]
    return ans

def ShiftRow(matrix):
    for i in range(len(matrix)):
        matrix[i] = RotateLeft(matrix[i], i)
    return matrix

def InverseShiftRow(matrix):
    for i in range(len(matrix)):
        matrix[i] = RotateRight(matrix[i], i)
    return matrix
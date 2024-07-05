import numpy

if __name__ == '__main__':
    SHAPES = [
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1, 1], [1, 1, 0]]
    ]
    shape = SHAPES[3]
    right = numpy.zeros((len(shape[0]), len(shape)), dtype=int)
    for i in range(len(shape)):
        new_i = len(shape) - i - 1
        for j in range(len(shape[0])):
            right[j][new_i] = shape[i][j]
    print(right)

    left = numpy.zeros((len(shape[0]), len(shape)), dtype=int)
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            new_j = len(shape[0]) - j - 1
            left[new_j][i] = shape[i][j]
    print(left)

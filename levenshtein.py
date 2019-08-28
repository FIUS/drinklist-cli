import numpy as np

def generalized_distance(firstWord, secondWord, w_insert, w_remove, w_replace_fn, w_insert_front_back):
    size_x = len(firstWord) + 1
    size_y = len(secondWord) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x * w_remove
    for y in range(size_y):
        matrix [0, y] = y * w_insert_front_back

    for x in range(1, size_x):
        for y in range(1, size_y):
            matrix [x,y] = min(
                matrix[x-1,y] + w_remove,
                matrix[x-1,y-1] + (0 if firstWord[x-1]==secondWord[y-1] else w_replace_fn(firstWord[x-1], secondWord[y-1])),
                matrix[x,y-1] + (w_insert_front_back if x==1 or x==len(firstWord) else w_insert)
            )
    return (matrix[size_x - 1, size_y - 1])

def distance(firstWord, secondWord):
    return generalized_distance(firstWord, secondWord, 1, 1, lambda x,y: 1, 1)

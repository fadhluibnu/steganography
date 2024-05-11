import numpy as np
import string
import random
unicode = list(" " + string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation)
print(len(unicode))

message = 'rizky albani'

def generate_random_matrix(rows, cols, min_val, max_val):
    # Menghasilkan matriks bilangan bulat acak
    try:
        random_matrix = np.random.randint(min_val, max_val + 1, size=(rows, cols))
        matrix_key_encrypt = []  
        for i in random_matrix.flatten():
            matrix_key_encrypt.append(unicode[int(i)])

        np.linalg.inv(random_matrix)

        return [random_matrix, matrix_key_encrypt, rows, cols]
    except Exception as e:
        return generate_random_matrix(rows, cols, min_val, max_val)

generate_size_matrix = random.randint(2,3)

matrix_key, matrix_key_encrypt, rows, cols = generate_random_matrix(generate_size_matrix, generate_size_matrix, 1, 3)
matrix_size = rows * cols
row_cols_encrypy = [unicode[rows], unicode[cols]]

encrypted = [row_cols_encrypy, matrix_key_encrypt]
encrypted = sum(encrypted, [])

def encrypt(message, rows, cols):
    print("\nEncode : ")
    encrypt_message = []
    for i in message:
        encrypt_message.append(unicode.index(i))

    matrix_message = []
    i = 0
    while i < len(encrypt_message):
        if i < len(encrypt_message):
            temp_matrix = encrypt_message[i:i+matrix_size]
            if len(temp_matrix) == matrix_size:
                matrix_message.append(temp_matrix)
            else:
                if len(temp_matrix) < rows:
                    lack = rows % len(temp_matrix)
                    while lack > 0:
                        temp_matrix.append(0)
                        lack -= 1
                else: 
                    lack = matrix_size - len(temp_matrix)
                    while lack > 0:
                        temp_matrix.append(0)
                        lack -= 1
                matrix_message.append(temp_matrix)
            i += matrix_size

    multiply_matrix = []
    for matrix in matrix_message:
        matrix = np.array(matrix)
        if len(matrix) == matrix_size:
            matrix = matrix.reshape(cols,rows)
        else:
            matrix = matrix.reshape(rows,1)
        multiply_matrix.append(np.matmul(matrix_key, matrix))

    print(multiply_matrix)

    for matrix in multiply_matrix:
        matrix = matrix.flatten()
        for item in matrix:
            if item < 95:
                encrypted.append(unicode[item])
                encrypted.append(unicode[0])
            else:
                many_reduce = 0
                while item >= 95:
                    item -= 95
                    many_reduce += 1
                encrypted.append(unicode[item])
                encrypted.append(unicode[many_reduce])

    return "".join(encrypted)

def decrypt(message):
    print("\nDecode :")
    message = list(message)
    rows = unicode.index(message[0])
    cols = unicode.index(message[1])
    del message[0:2]

    key_encrypt = message[0:rows * cols]
    key = []
    for item in key_encrypt:
        key.append(unicode.index(item))
    key = np.array(key)
    key = key.reshape(rows, cols)
    print("key : ", key)
    key = np.linalg.inv(key)
    del message[0:rows * cols]

    transform_message = []
    for item in message:
        transform_message.append(unicode.index(item)) 
    
    print(transform_message)
    
    real_result = []
    i = 0
    while i < len(transform_message):
        item = transform_message[i]
        many_reduce = transform_message[i+1]
        while many_reduce > 0:
            item += 95
            many_reduce -= 1
        real_result.append(item)
        i += 2
    
    print(real_result)
    
    matrix_message = []
    i = 0
    while i < len(real_result):
        if i < len(real_result):
            temp_matrix = real_result[i:i+matrix_size]
            if len(temp_matrix) == matrix_size:
                matrix_message.append(temp_matrix)
            else:
                if len(temp_matrix) < rows:
                    lack = rows % len(temp_matrix)
                    while lack > 0:
                        temp_matrix.append(0)
                        lack -= 1
                else: 
                    lack = matrix_size - len(temp_matrix)
                    while lack > 0:
                        temp_matrix.append(0)
                        lack -= 1
                matrix_message.append(temp_matrix)
            i += matrix_size

    print(matrix_message)

    multiply_matrix = []
    for matrix in matrix_message:
        matrix = np.array(matrix)
        if len(matrix) == matrix_size:
            matrix = matrix.reshape(cols,rows)
        else:
            matrix = matrix.reshape(rows,1)
        multiply_matrix.append(np.matmul(key, matrix))
    print(multiply_matrix)

    decrypted = []
    for matrix in multiply_matrix:
        matrix = matrix.flatten()
        for item in matrix:
            decrypted.append(unicode[round(item)])

    return "".join(decrypted)
    


enkripsi = encrypt(message, rows, cols)
print(enkripsi)

dekripsi = decrypt(enkripsi)
print(dekripsi)

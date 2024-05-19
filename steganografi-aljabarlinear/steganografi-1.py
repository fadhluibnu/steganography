import cv2
import numpy as np
import string
import random

unicode = list(" " + string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation)
print(len(unicode))

# message = 'Aku adalah seorang pilot. Pesawat saya terbang dari Indonesia Ke Arab Saudi.'

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


def encrypt(message):
    generate_size_matrix = random.randint(2,3)

    matrix_key, matrix_key_encrypt, rows, cols = generate_random_matrix(generate_size_matrix, generate_size_matrix, 1, 3)

    encrypted = []
    
    encrypted.append([unicode[rows], unicode[cols]])
    encrypted.append(matrix_key_encrypt)

    encrypted = sum(encrypted, [])

    matrix_size = rows * cols

    print("\nEncode : ")
    print("key : " , matrix_key)
    encrypt_message = []
    for i in message:
        encrypt_message.append(unicode.index(i))
    
    print("encrypt_message : ")
    print(encrypt_message)

    matrix_message = []
    i = 0
    while i < len(encrypt_message):
        if i < len(encrypt_message):
            temp_matrix = encrypt_message[i:i+matrix_size]
            if len(temp_matrix) == matrix_size:
                print(temp_matrix)
                matrix_message.append(temp_matrix)
            else:
                lack = matrix_size  - len(temp_matrix)
                while lack > 0:
                    temp_matrix.append(0)
                    lack -= 1
                matrix_message.append(temp_matrix)
            i += matrix_size
        
    print("matrix_message : ")
    print(matrix_message)

    multiply_matrix = []
    for matrix in matrix_message:
        matrix = np.array(matrix)
        if len(matrix) == matrix_size:
            matrix = matrix.reshape(cols, rows)
        else:
            matrix = matrix.reshape(rows,1)
        multiply_matrix.append(np.matmul(matrix_key, matrix))

    print("multiply_matrix : ")
    print(multiply_matrix)

    for matrix in multiply_matrix:
        matrix = matrix.flatten()
        for item in matrix:
            if item < 95:
                encrypted.append(unicode[item ])
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
    matrix_size  = rows * cols
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
    
    print("transform_message : ")
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
    
    print("real_result : ")
    print(real_result)
    
    matrix_message = []
    i = 0
    while i < len(real_result):
        if i < len(real_result):
            temp_matrix = real_result[i:i+matrix_size]
            if len(temp_matrix) == matrix_size:
                matrix_message.append(temp_matrix)
            else:
                lack = matrix_size  - len(temp_matrix)
                while lack > 0:
                    temp_matrix.append(0)
                    lack -= 1
                matrix_message.append(temp_matrix)
            i += matrix_size

    print("matrix_message : ")
    print(matrix_message)

    multiply_matrix = []
    for matrix in matrix_message:
        matrix = np.array(matrix)
        if len(matrix) == matrix_size:
            matrix = matrix.reshape(cols,rows)
        else:
            matrix = matrix.reshape(rows,1)
        multiply_matrix.append(np.matmul(key, matrix))
    
    print("multiply_matrix : ")
    print(multiply_matrix)

    decrypted = []
    for matrix in multiply_matrix:
        matrix = matrix.flatten()
        for item in matrix:
            decrypted.append(unicode[round(item)])

    return "".join(decrypted)


# Fungsi untuk mengonversi teks menjadi representasi biner menggunakan ASCII
def text_to_binary(text):
    binary_text = ""
    for char in text:
        # Konversi karakter ke kode ASCII
        ascii_code = ord(char)
        # Konversi kode ASCII ke representasi biner dengan padding nol di depan
        binary_char = format(ascii_code, '08b')
        # Gabungkan representasi biner dari setiap karakter
        binary_text += binary_char
    return binary_text


def binary_to_text(binary_string):
    # Pastikan panjang string biner adalah kelipatan 8
    if len(binary_string) % 8 != 0:
        raise ValueError("Panjang string biner harus kelipatan 8.")

    # Pisahkan string biner menjadi potongan-potongan 8 bit
    binary_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    # Konversi setiap potongan biner menjadi karakter ASCII
    characters = ''.join([chr(int(chunk, 2)) for chunk in binary_chunks])

    return characters


# Fungsi untuk menyisipkan pesan biner ke dalam gambar menggunakan LSB
def embed_message(id, path, file_name, message):
    binary_message = text_to_binary(message + '(**)')
    image = cv2.imread(path+file_name)
    height, width, _ = image.shape
    message_index = 0

    for y in range(height):
        for x in range(width):
            # Dapatkan nilai piksel
            pixel = list(image[y, x])
            # Loop melalui setiap saluran warna (R, G, B)
            for c in range(3):
                # Ubah 2 bit terakhir menjadi bit pesan
                pixel[c] = (pixel[c] & 0b11111100) | int(binary_message[message_index:message_index+2], 2)
                # Pindah ke bit pesan berikutnya
                message_index += 2
                # Jika pesan telah disisipkan semua, kembalikan gambar yang dimodifikasi
                if message_index >= len(binary_message):
                    image[y, x] = tuple(pixel)
                    cv2.imwrite('embedded_image/embedded_' + file_name, image)
                    return 'embedded_image/embedded_' + file_name
            # Simpan nilai piksel yang telah dimodifikasi
            image[y, x] = tuple(pixel)
    return 'embedded_image/embedded_' + file_name


def extract_message(path):
    img = cv2.imread(path)
    height, width, _ = img.shape

    binary_message = ''
    found_delimiter = False

    for y in range(height):
        for x in range(width):
            r, g, b = img[y, x]
            # Ambil 2 bit terakhir (LSB) dari setiap saluran warna (RGB)
            binary_message += format(r & 0b11, '02b')
            binary_message += format(g & 0b11, '02b')
            binary_message += format(b & 0b11, '02b')

            # Cek apakah terdapat delimiter
            if len(binary_message) % 8 == 0:
              if '(**)' in binary_to_text(binary_message):
                found_delimiter = True
                break

        if found_delimiter:
            break

    return binary_to_text(binary_message).split('(**)')[0]


# path = 'original_image/'
# message = '1234'

# enkripsi = encrypt(message)
# print(enkripsi)

# embedded_image = embed_message("2", path, 'majelisazzahir_1710878115127.jpeg', enkripsi)

# extranct_image = extract_message('embedded_image/embedded_majelisazzahir_1710878115127.jpeg')

# decode = decrypt(extranct_image)

# print(decode)

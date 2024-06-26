import cv2
import numpy as np
import string
import random

unicode = list(
    " " + 
    string.ascii_uppercase + 
    string.ascii_lowercase + 
    string.digits + 
    string.punctuation
)

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
    
    print("\nEncode : ")
    print("key : " , matrix_key)
    
    len_message = len(message)
    kurang = 0
    if len_message > rows:
        kurang = rows - (len_message % rows)
    else :
        kurang = rows - len_message
        
    while kurang > 0:
        message += " "
        kurang -= 1
    
    matrix_message = []
    for i in message:
        matrix_message.append(unicode.index(i))
    print(matrix_message)
    
    matrix_message = np.array(matrix_message)
    matrix_message = matrix_message.reshape(rows, len(matrix_message) // rows)
    
    multiply = np.matmul(matrix_key, matrix_message)
    
    
    multiply = multiply.flatten()
    print(multiply)
    
    encrypt_matriks = []
    for item in multiply:
        reduce = 0
        while item >= 95:
            reduce = item // 95
            item = item % 95 
        
        encrypt_matriks.append(unicode[item])    
        encrypt_matriks.append(unicode[reduce]) 
    
    print(encrypt_matriks)   
    
    encrypted.append(encrypt_matriks)
    encrypted = sum(encrypted, [])

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

    print(list(message))

    transform_message = []
    for item in message:
        transform_message.append(unicode.index(item)) 
    print(transform_message)
    
    matrix_message = []
    idx = 0
    while idx < len(transform_message):
        item = transform_message[idx] + (95 * transform_message[idx + 1])
        matrix_message.append(item)
        idx += 2
        
    print(matrix_message)
    
    matrix_message = np.array(matrix_message)
    matrix_message = matrix_message.reshape(rows, len(matrix_message) // rows)
    
    multiply = np.matmul(key, matrix_message)
    
    multiply = multiply.flatten()
    
    print(multiply)
    
    decrypted = []
    for item in multiply:
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
message = '1234'

enkripsi = encrypt(message)
print(enkripsi)

# embedded_image = embed_message("2", path, 'majelisazzahir_1710878115127.jpeg', enkripsi)

# extranct_image = extract_message('embedded_image/embedded_majelisazzahir_1710878115127.jpeg')

decode = decrypt(enkripsi)

print(decode)

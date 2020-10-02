from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import pad, unpad
from bitstring import BitArray
import time
import os

def calculate_throughput(total_time, data_size):
    per_byte = data_size/total_time
    per_bit = (data_size * 8)/total_time
    
    return per_byte, per_bit

def encrypt_des_ecb(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = b"\x00\x00\x00\x00\x00\x00\x00\x10" #0000000000000000000000000000000000000000000000000000000000000010
    cipher = DES.new(key, DES.MODE_ECB)

    #print(len(p_bytes))
    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE)) #use unpad(msg, BLOCK_SIZE) after decrypting
    #print(msg)

    with open("des_ecb.txt", 'ab') as output_file:
        output_file.write(msg)

def decrypt_des_ecb(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = b"\x00\x00\x00\x00\x00\x00\x00\x10"
    decipher = DES.new(key, DES.MODE_ECB)
    msg = decipher.decrypt(p_bytes)

    with open("des_ecb_decrypt.txt", 'ab') as output_file:
        output_file.write(msg)

des_iv = None
def encrypt_des_cbc(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = b"\x00\x00\x00\x00\x00\x00\x00\x10" #0000000000000000000000000000000000000000000000000000000000000010
    cipher = DES.new(key, DES.MODE_CBC, iv=des_iv)

    #print(len(p_bytes))
    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE)) #use unpad(msg, BLOCK_SIZE) after decrypting
    #print(msg)

    with open("des_cbc.txt", 'ab') as output_file:
        output_file.write(msg)

def decrypt_des_cbc(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = b"\x00\x00\x00\x00\x00\x00\x00\x10"
    decipher = DES.new(key, DES.MODE_CBC, iv=des_iv)
    print(des_iv)
    msg = decipher.decrypt(p_bytes)

    with open("des_cbc_decrypt.txt", 'ab') as output_file:
        output_file.write(msg)

def encrypt_3des_ecb(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = DES3.adjust_key_parity("abcdefghijklmnop".encode('utf8'))
    cipher = DES3.new(key, DES3.MODE_ECB)

    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE))
    

    with open("des3_ecb.txt", 'ab') as output_file:
        output_file.write(msg)

def decrypt_3des_ecb(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = DES3.adjust_key_parity("abcdefghijklmnop".encode('utf8'))
    decipher = DES3.new(key, DES3.MODE_ECB)
    msg = decipher.decrypt(p_bytes)
    

    with open("des3_ecb_decrypt.txt", 'ab') as output_file:
        output_file.write(msg)

def encrypt_3des_cbc(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = DES3.adjust_key_parity("abcdefghijklmnop".encode('utf8'))
    cipher = DES3.new(key, DES3.MODE_CBC)

    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE))

    with open("des3_cbc.txt", 'ab') as output_file:
        output_file.write(msg)

def decrypt_3des_cbc(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = DES3.adjust_key_parity("abcdefghijklmnop".encode('utf8'))
    decipher = DES3.new(key, DES3.MODE_CBC)
    msg = decipher.decrypt(p_bytes)
    

    with open("des3_cbc_decrypt.txt", 'ab') as output_file:
        output_file.write(msg)

def encrypt_aes_ecb(p_bytes):
    BLOCK_SIZE = 16 #bytes
    key = "abcdefghijklmnop"
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE))

    with open("aes_ecb.txt", 'ab') as output_file:
        output_file.write(msg)

def decrypt_aes_ecb(p_bytes):
    BLOCK_SIZE = 16 # bytes
    key = "abcdefghijklmnop"
    decipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    msg = decipher.decrypt(p_bytes)
    

    with open("aes_ecb_decrypt.txt", 'ab') as output_file:
        output_file.write(msg)

def encrypt_aes_cbc(p_bytes):
    BLOCK_SIZE = 16 #bytes
    key = "abcdefghijklmnop"
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC)
    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE))

    with open("aes_cbc.txt", 'ab') as output_file:
        output_file.write(msg)

def decrypt_aes_cbc(p_bytes):
    BLOCK_SIZE = 16 # bytes
    key = "abcdefghijklmnop"
    decipher = AES.new(key.encode('utf8'), AES.MODE_CBC)
    msg = decipher.decrypt(p_bytes)
    

    with open("aes_cbc_decrypt.txt", 'ab') as output_file:
        output_file.write(msg)

def encrypt(encrypt_fn):
    total_time = 0
    data_size = 0 #in bytes

    buffer_size = 65536 # bytes, 64 kb
    
    with open("plain.txt", "rb") as f:    
        p_bytes = f.read(buffer_size)
        #counter = 0
        while len(p_bytes) > 0:
            #get start time
            start_time = time.time()

            #encrypt
            encrypt_fn(p_bytes)

            #get end time
            end_time = time.time()

            #add total time and data calculations
            total_time += (end_time - start_time)
            
            data_size += len(p_bytes) # bytes

            #repeat the process for the next set of bytes
            p_bytes = f.read(buffer_size)

    throughput_in_bytes, throughput_in_bits = calculate_throughput(total_time, data_size)
    return throughput_in_bytes, throughput_in_bits

def decrypt(decrypt_fn, file_to_open):
    total_time = 0
    data_size = 0 #in bytes

    buffer_size = 65536 # bytes, 64 kb
    
    with open(file_to_open, "rb") as f:
        p_bytes = f.read(buffer_size)
        #counter = 0
        while len(p_bytes) > 0:
            #get start time
            start_time = time.time()

            #decrypt
            decrypt_fn(p_bytes)

            #get end time
            end_time = time.time()

            #add total time and data calculations
            total_time += (end_time - start_time)
            
            data_size += len(p_bytes) # bytes

            #repeat the process for the next set of bytes
            p_bytes = f.read(buffer_size)

    throughput_in_bytes, throughput_in_bits = calculate_throughput(total_time, data_size)
    return throughput_in_bytes, throughput_in_bits

#remove all text files from previous runs
path_names = ["aes_cbc.txt", "aes_cbc_decrypt.txt",
              "aes_ecb.txt", "aes_ecb_decrypt.txt",
              "des_cbc.txt", "des_cbc_decrypt.txt",
              "des_ecb.txt", "des_ecb_decrypt.txt",
              "des3_cbc.txt", "des3_cbc_decrypt.txt",
              "des3_ecb.txt", "des3_ecb_decrypt.txt"]
for path in path_names:
    if os.path.exists(path):
        os.remove(path)
    

#DES
throughput_in_bytes, throughput_in_bits = encrypt(encrypt_des_ecb)
print("DES ECB Mode Encryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = decrypt(decrypt_des_ecb, "des_ecb.txt")
print("DES ECB Mode Decryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = encrypt(encrypt_des_cbc)
print("DES CBC Mode Encryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = decrypt(decrypt_des_cbc, "des_cbc.txt")
print("DES CBC Mode Decryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()


#3DES
throughput_in_bytes, throughput_in_bits = encrypt(encrypt_3des_ecb)
print("3DES ECB Mode Encryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = decrypt(decrypt_3des_ecb, "des3_ecb.txt")
print("3DES ECB Mode Decryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = encrypt(encrypt_3des_cbc)
print("3DES CBC Mode Encryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = decrypt(decrypt_3des_cbc, "des3_cbc.txt")
print("3DES CBC Mode Decryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

#AES
throughput_in_bytes, throughput_in_bits = encrypt(encrypt_aes_ecb)
print("AES ECB Mode Encryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = decrypt(decrypt_aes_ecb, "aes_ecb.txt")
print("AES ECB Mode Decryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = encrypt(encrypt_aes_cbc)
print("AES CBC Mode Encryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

throughput_in_bytes, throughput_in_bits = decrypt(decrypt_aes_cbc, "aes_cbc.txt")
print("AES CBC Mode Decryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()

"""
key = b'-8B key-'
cipher = DES.new(key, DES.MODE_OFB)
plaintext = b'sona si latine loqueris '
msg = cipher.iv + cipher.encrypt(plaintext)
print(msg) #print(msg.hex())

key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_EAX)

nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)
print(ciphertext)
"""

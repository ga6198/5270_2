from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
from bitstring import BitArray
import time

def calculate_throughput(total_time, data_size):
    per_byte = data_size/total_time
    per_bit = (data_size * 8)/total_time
    
    return per_byte, per_bit

def encrypt_des_ecb(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = b"\x00\x00\x00\x00\x00\x00\x00\x10" #0000000000000000000000000000000000000000000000000000000000000010
    cipher = DES.new(key, DES.MODE_ECB)

    print(len(p_bytes))
    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE)) #use unpad(msg, BLOCK_SIZE) after decrypting
    print(msg)

    with open("des_ecb.txt", 'wb') as output_file:
        output_file.append(msg)

def encrypt_des_cbc(p_bytes):
    BLOCK_SIZE = 8 # bytes
    key = b"\x00\x00\x00\x00\x00\x00\x00\x10" #0000000000000000000000000000000000000000000000000000000000000010
    cipher = DES.new(key, DES.MODE_CBC)

    print(len(p_bytes))
    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE)) #use unpad(msg, BLOCK_SIZE) after decrypting
    print(msg)

    with open("des_ecb.txt", 'wb') as output_file:
        output_file.append(msg)

def encrypt_aes_ecb(p_bytes):
    BLOCK_SIZE = 16 #bytes
    key = "abcdefgh"
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    msg = cipher.encrypt(pad(p_bytes, BLOCK_SIZE))

    with open("aes_ecb.txt", 'wb') as output_file:
        output_file.append(msg)
    

def encrypt(encrypt_fn, bytes_to_read):
    total_time = 0
    data_size = 0 #in bytes
    with open("plain.txt", "rb") as f:    
        p_bytes = f.read(bytes_to_read)
        #counter = 0
        while p_bytes:
            #counter += 1
            #print(counter)
            #print(p_bytes)

            #get start time
            start_time = time.time()

            #encrypt
            #msg = des_cipher.encrypt(p_bytes)
            #print(msg)
            encrypt_fn(p_bytes)

            #get end time
            end_time = time.time()

            #add total time and data calculations
            total_time += (end_time - start_time)
            
            data_size += bytes_to_read # bytes

            #repeat the process for the next 8 bytes
            p_bytes = f.read(bytes_to_read)

    throughput_in_bytes, throughput_in_bits = calculate_throughput(total_time, data_size)
    return throughput_in_bytes, throughput_in_bits

#DES
buffer_size = 65536 # bytes, 64 kb
with open("plain.txt", "rb") as f:
    buffer = f.read(buffer_size)

    while len(buffer) > 0:

        BLOCK_SIZE = 8 # bytes
        key = b"\x00\x00\x00\x00\x00\x00\x00\x10" #0000000000000000000000000000000000000000000000000000000000000010
        cipher = DES.new(key, DES.MODE_ECB)

        #print(len(p_bytes))
        msg = cipher.encrypt(pad(buffer, BLOCK_SIZE)) #use unpad(msg, BLOCK_SIZE) after decrypting
        print(msg)
        print(len(buffer))
        buffer = f.read(buffer_size)

        

"""
throughput_in_bytes, throughput_in_bits = encrypt(encrypt_des_ecb, 8)
print("DES Encryption Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()
"""

#3DES

#AES
"""
throughput_in_bytes, throughput_in_bits = encrypt(encrypt_aes_ecb, 16)
print("DES Throughput")
print(throughput_in_bytes, "bytes per second")
print(throughput_in_bits, "bits per second")
print()
"""

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

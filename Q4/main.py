from Crypto.Cipher import DES, AES
from bitstring import BitArray

#from Crypto.Random import get_random_bytes
#key = get_random_bytes(32) # 32 bytes * 8 = 256 bits (1 byte = 8 bits)
#print(key)

#key = "0000000000000000000000000000000000000000000000000000000000000010"
key = b"\x00\x00\x00\x00\x00\x00\x00\x10"
print(key)
cipher = DES.new(key, DES.MODE_ECB)
#plaintext = "0000000000000000000000000000000000000000000000000000000000000000"
plaintext = b"\x00\x00\x00\x00\x00\x00\x00\x00"

msg = cipher.encrypt(plaintext) #bytes object
#print(msg)
#conversion from bytes to bits
c = BitArray(hex=msg.hex())
print(c.bin)

des_key = b"\x00\x00\x00\x00\x00\x00\x00\x10" #0000000000000000000000000000000000000000000000000000000000000010
des_cipher = DES.new(key, DES.MODE_ECB)

with open("plain.txt", "rb") as f:    
    """
    plaintext = f.read()
    p_bytes = plaintext.encode('utf-8')
    #print(p_bytes)

    msg = des_cipher.encrypt(des_key)
    print(msg)
    c = BitArray(hex=msg.hex())
    print(c.bin)
    
    #print(plaintext)
    """
    p_bytes = f.read(8)
    counter = 0
    while p_bytes:
        counter += 1
        print(counter)
        p_bytes = f.read(8)


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

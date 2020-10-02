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

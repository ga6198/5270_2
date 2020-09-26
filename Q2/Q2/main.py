#from Crypto.Cipher import DES
from collections import deque
import textwrap

def xor(string1, string2):
    result = ""
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            result += "1"
        else:
            result += "0"
    return result

####Key Generation####

#left shift function. Shift_amount takes 1 or 2s
def left_shift(key, shift_amount):
    d = deque(key)
    if shift_amount == 1:
        d.rotate(-1) #rotate left by 1
    elif shift_amount == 2:
        d.rotate(-2) #rotate left by 2
    return ''.join(d) #return the deque as a string

def create_round_keys(key):
    #Permutated choice 1 table
    permutated_choice_1 = (
        57,49,41,33,25,17,9, 
	1,58,50,42,34,26,18, 
	10,2,59,51,43,35,27, 
	19,11,3,60,52,44,36,		 
	63,55,47,39,31,23,15, 
	7,62,54,46,38,30,22, 
	14,6,61,53,45,37,29, 
	21,13,5,28,20,12,4 )

    #Permutated choice 2 table
    permutated_choice_2 = (
        14,17,11,24,1,5, 
	3,28,15,6,21,10, 
	23,19,12,4,26,8, 
	16,7,27,20,13,2, 
	41,52,31,37,47,55, 
	30,40,51,45,33,48, 
	44,49,39,56,34,53, 
	46,42,50,36,29,32 
        )

    #get the 56 bit key with permutated choice 1 table
    pc1_key = ""
    for i in range(len(permutated_choice_1)):
        perm_index = permutated_choice_1[i] - 1 #need to subtract 1 bc pc1 table has positions, not indices
        perm_value = key[perm_index]
        pc1_key += perm_value

    #print(pc1_key)

    #divide key into 28 bit parts
    left_key = pc1_key[:28]
    right_key = pc1_key[28:]

    #print(left_key)
    #print(right_key)

    #holds round keys
    round_keys = []

    #create the 16 round keys
    for i in range(16):
        #need to circular shift both the left and right keys
        #left_shift by one when index is 0, 1, 8, or 15
        if (i == 0 or i == 1 or i == 8 or i == 15):
            left_key = left_shift(left_key, 1)
            right_key = left_shift(right_key, 1)
        #left_shift by two when index is 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14
        else:
            left_key = left_shift(left_key, 2)
            right_key = left_shift(right_key, 2)

        #use both keys parts with permutated choice 2 table to get round function
        full_key = left_key + right_key

        round_key = ""
        for j in range(len(permutated_choice_2)):
            perm_index = permutated_choice_2[j] - 1 #need to subtract 1 bc pc2 table has positions, not indices
            perm_value = full_key[perm_index]
            round_key += perm_value

        round_keys.append(round_key)
        #print("Key for round", i + 1, ":", round_key)

    return round_keys

def des_encrypt(plaintext, round_keys):
    #expansion table
    expansion_table = (
        32,1,2,3,4,5,4,5, 
	6,7,8,9,8,9,10,11, 
	12,13,12,13,14,15,16,17, 
	16,17,18,19,20,21,20,21, 
	22,23,24,25,24,25,26,27, 
	28,29,28,29,30,31,32,1
        )

    #s-boxes
    s_boxes = (
        (
            (14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7),
            (0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8),
            (4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0),
            (15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13)
        ),
        
        (
            (15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10),
            (3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5),
            (0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15),
            (13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9)
        ),
        
        (
            (10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8),
            (13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1),
            (13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7),
            (1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12)
        ),
        
        (
            (7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15),
            (13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9),
            (10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4),
            (3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14)
        ),
        
        (
            (2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9),
            (14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6),
            (4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14),
            (11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3)
        ),
        
        (
            (12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11),
            (10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8),
            (9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6),
            (4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13)
        ),
        
        (
            (4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1),
            (13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6),
            (1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2),
            (6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12)
        ),
        
        (
            (13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7),
            (1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2),
            (7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8),
            (2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11)
        )
    )

    #permutation_table
    permutation_table = (
        16,7,20,21,29,12,28,17, 
	1,15,23,26,5,18,31,10, 
	2,8,24,14,32,27,3,9,
	19,13,30,6,22,11,4,25 
        )

    #skip the initial permutation

    #only perform the round functions
    #split 64bit plaintext in half
    left = plaintext[:32]
    right = plaintext[32:]

    #apply the 16 round functions
    for i in range(16):
        #many operations applied to right half
        #apply expansion table
        expanded_right = ""
        for j in range(len(expansion_table)):
            perm_index = expansion_table[j] - 1
            perm_value = right[perm_index]
            expanded_right += perm_value

        #xor expanded_right against the current round key (will be 0s and 1s)
        xor_right = xor(round_keys[0], expanded_right)
        #print(xor_right)

        #divide into 8 6-bit parts and apply s-boxes
        s_box_result = ""
        parts = textwrap.wrap(xor_right, 6)
        for j in range(len(parts)):
            row_index = parts[j][0] + parts[j][5] #bit 1 and bit 6
            col_index = parts[j][1] + parts[j][2] + parts[j][3] + parts[j][4] #bit 2, 3, 4, 5

            #convert row and col indices to decimal
            row_index = int(row_index, 2)
            col_index = int(col_index, 2)

            s_box_val = s_boxes[j][row_index][col_index]
            #print(s_box_val)

            bin_result = format(s_box_val, "b")

            while len(bin_result) < 4: #add extra 0s if result is not 4 bits
                  bin_result = "0" + bin_result

            #print(bin_result)
            s_box_result += bin_result

        #final permutation
        perm2 = ""
        for j in range(len(permutation_table)):
            perm_index = permutation_table[j] - 1
            perm_value = s_box_result[perm_index]
            perm2 += perm_value

        #final xor
        xor_left_right = xor(perm2, left)

        #round_result = right + xor_left_right
        #print("Round", i + 1, "Result:", round_result)

        #swap left and right
        left = xor_left_right #on the final round,left will have this value 
        if i < 15: #don't need to swap on final round
            temp = right
            right = xor_left_right
            left = temp

        round_result = left + right
        print("Round", i + 1, "Result:", round_result)

    #skip the 32-bit swap

    #skip the inverse initial permutation

    ciphertext = left + right
    return ciphertext

if __name__ == "__main__":
    #key = "1234"
    #print(left_shift(key, 1))
    #print(left_shift(key, 2))

    #key = "1234567890123456789012345678901234567890123456789012345678901234"
    #round_keys = create_round_keys(key)

    #plain1 = "1010101111001101111001101010101111001101000100110010010100110110"
    #print(des_encrypt(plain1, round_keys))
    k1 = "0000000000000000000000000000000000000000000000000000000000000010"
    m1 = "0000000000000000000000000000000000000000000000000000000000000000"

    print("Key 1")
    print(k1)
    print("Plaintext 1")
    print(m1)

    round_keys1 = create_round_keys(k1)
    answer1 = des_encrypt(m1, round_keys1)

    print()

    k2 = "0000000000000000000000000000000000000000000000000000000000000000"
    m2 = "0000000000000000000000000000000000000000000000000000000000000010"

    print("Key 2")
    print(k2)
    print("Plaintext 2")
    print(m2)

    round_keys2 = create_round_keys(k2)
    answer2 = des_encrypt(m2, round_keys2)

    print()

    k3 = "0000000000000000000000000000000000000000000000000000000000000010"
    m3 = "0000000000000000000000000000000000000000000000000000000000000001"

    print("Key 3")
    print(k3)
    print("Plaintext 3")
    print(m3)

    round_keys3 = create_round_keys(k3)
    answer3 = des_encrypt(m3, round_keys3)

    print()

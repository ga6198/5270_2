def get_permutation(word, permutation):
    new_string = ""

    for i in range(len(permutation)):
        current_perm_index = permutation[i]
        new_string += word[current_perm_index]

    return new_string

def get_inverse(word, permutation):
    inverse_numbers = []

    for i in range(len(permutation)):
        #looking through permutation again and finding, 0, 1, 2, etc (i)

        for j in range(len(permutation)):
            # if the number i is found at an index j, j is our inverse number
            if (permutation[j] == i):
                inverse_numbers.append(j)
                break

    return inverse_numbers, get_permutation(word, inverse_numbers)

          
if __name__ == "__main__":
    print("Permutation and Inverse Permutation")
    n = int(input("Enter a size n: "))
    word = input("Enter a word of size n: ")

    while len(word) != n:
        word = input("Enter a word of size n: ")

    print("Input a permutation by typing numbers, separated by spaces")
    print("Available Numbers: ", end = '')
    for num in range(n):
        print(str(num), end = " ")

    print()
    permutation_string = input()
    permutation_numbers = permutation_string.split()
    permutation_numbers = map(int, permutation_numbers)
    permutation_numbers = list(permutation_numbers)
    #print(permutation_numbers)

    permutation = get_permutation(word, permutation_numbers)
    print("Permutation:", permutation)

    inverse_permutation_numbers, inverse_permutation = get_inverse(permutation, permutation_numbers)
    print("Inverse Permutation:", inverse_permutation)
    print("Inverse Permutation Numbers:", inverse_permutation_numbers)

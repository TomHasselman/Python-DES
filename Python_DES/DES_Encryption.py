import re #for regular expressions
import os #for finding working directory so that the path for the plaintext file can be found

#The following tables are taken from FIPS PUB 46-3. They are permutation tables used in the DES algorithm
pc1 = [
  57, 49, 41, 33, 25, 17, 9,
  1, 58, 50, 42, 34, 26, 18, 
  10, 2, 59, 51, 43, 35, 27, 
  19, 11, 3, 60, 52, 44, 36, 
  
  63, 55, 47, 39, 31, 23, 15, 
  7, 62, 54, 46, 38, 30, 22, 
  14, 6, 61, 53, 45, 37, 29, 
  21, 13, 5, 28, 20, 12, 4
]

pc2 = [ 14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32,
]

left_shift_list = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

ip = [  58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19,11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
]

ip_inverse = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
]

expansion_table = [ 32, 1, 2, 3, 4, 5, 
                    4, 5, 6, 7, 8, 9, 
                    8, 9, 10, 11, 12, 13,
                    12, 13, 14, 15, 16, 17,
                    16, 17, 18, 19, 20, 21, 
                    20, 21, 22, 23, 24, 25, 
                    24, 25, 26, 27, 28, 29, 
                    28, 29, 30, 31, 32, 1
]


#The sboxes are placed in a list so that it's easy to access the correct sbox at the correct time
sbox_list = [

    #sbox1 
    [
    [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
    [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
    [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
    [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],

    #sbox2 
    [
    [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
    [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
    [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
    [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],

    #sbox3
    [
    [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
    [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
    [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
    [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]   
    ],

    #sbox4
    [
    [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
    [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
    [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
    [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],

    #sbox5
    [
    [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
    [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
    [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
    [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],

    #sbox6
    [
    [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
    [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
    [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
    [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],

    #sbox7
    [
    [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
    [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
    [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
    [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]    
    ],

    #sbox8
    [
    [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
    [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
    [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
    [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]

p_table = [
            16, 7, 20, 21,
            29, 12, 28, 17,
            1, 15, 23, 26,
            5, 18, 31, 10,
            2, 8, 24, 14,
            32, 27, 3, 9,
            19, 13, 30, 6,
            22, 11, 4, 25
]


list_of_keys = []


def string_to_binary(input_string):
    """Takes a string as input and outputs the binary representation of it.
        Represents each ASCII character as an 8-bit value"""
        
    character_list = list(input_string)
    
    return_string = ''
    
    for character in character_list:
        decimal_value = ord(character)
        binary_value = bin(decimal_value)[2:].zfill(8) # bin() prepends "0b" to the value, so slice it off. 
                                                       #Then pad with zero so that the value is 8 bits
        return_string += binary_value
        
    return return_string

def key_string_to_binary(input_string):
    """Takes a string as input and outputs the binary representation of it, 
    appending '0' if the parity is odd and '1' if the parity is even."""
    
    character_list = list(input_string)
    
    return_string = ''
    
    for character in character_list:
        parity = parity_check(character)
        
        decimal_value = ord(character)
        binary_value = bin(decimal_value)[2:]
        
        if parity == '0':
            return_string += binary_value+'0'
        else:
            return_string += binary_value+'1'
            
    return return_string
    
def parity_check(character):
    """Determines whether the binary representation of the character has an even or odd number of 1's.
        Returns '0' if the parity is odd and '1' if the parity is even."""
    decimal_value = ord(character)
    binary_value = bin(decimal_value)[2:]
    binary_value = list(binary_value)
    count = 0
    for bit in binary_value:
        if bit == '1':
            count += 1
    if count % 2 == 0:
        return '1' #even parity
    else:
        return '0' #odd parity   
    
def permute(input_string, table):
    """takes a string and permutation table as parameters and permutes the string according to the permutation table.
        returns a list which is the permuted string"""
    
    temp_list = []
    
    for index in range(len(table)):
        target_pos = table[index] - 1 #the values in the permutation table are "places", not indices, so fix that
        temp_list.append(input_string[target_pos])
        
    return temp_list

def permute_list_of_blocks(list_to_permute, table):
    """takes a list of blocks and a permutation table as parameters.
        Then called the permute() function to permute each block in the list."""
    temp_list = []
    
    for block in list_to_permute:
        block = permute(block, table)
        temp_list.append(block)
        print(f"Initial permutation: {''.join(block)}")
        output_file.write(f"Initial permutation: {''.join(block)}\n")
        
    return temp_list

def subkey_generation(key_string, list_to_add_to):
    """Takes a ket in the form of a string and creates a list of 16 subkeys.
        The key is split into two halves before being left shifted accoring to the list left_shift_list.
        The entire subkey is then permuted by the pc2 table and added to the list_to_add_to list"""
    key_left = key_string[:28] #first 28 bits
    key_right = key_string[28:] #last 28 bits

    for i in range(16):
        shifts = left_shift_list[i]
        
        key_left = key_left[shifts:] + key_left[:shifts] #shift left by the number of shifts
        key_right = key_right[shifts:] + key_right[:shifts] #shift left by the number of shifts
        
        list_to_add_to.append(permute(key_left + key_right, pc2))
        
        print(f"Subkey number {i+1} is: {''.join(list_to_add_to[i])}")
        output_file.write(f"Subkey number {i+1} is: {''.join(list_to_add_to[i])}\n")
        
    

def strip_string(input_string):
    """Removes all non-alphanumeric characters from the input string"""
    return re.sub(r'\W+', '', input_string)
    
def make_block(input_string, size):
    """Takes an string of binary data and breaks it into 64-bit chunks"""
    return input_string[:size]
        
def make_list_of_blocks(input_string, size):
    """Calls 'make_block()' multiple time to split the input_string into multiple 64-bit blocks. 
        Appends '0' to the end of the final block so that all blocks are uniform size. 
        Returns a list of 64-bit blocks."""
    list_of_blocks = []
    
    for i in range(0, len(input_string), size):
        list_of_blocks.append(input_string[i:i+size])
        
    #check if the last block is the correct size. If not, append '0' to the end of the block    
    if list_of_blocks[-1] != size:
        list_of_blocks[-1] = list_of_blocks[-1].ljust(size, '0')
        
    return list_of_blocks

def pretty_print_data(block_list, size):
    """Takes a list of blocks and prints them in their byte form"""
    
    for block in block_list:
        for i in range(0,len(block),size):
            print(block[i:i+size])
            output_file.write(block[i:i+size]+"\n")
            
def encipher_function(block, key):
    """The main function that performs DES.
        Takes a 64-bit block and a 64-bit key as parameters.
        returns the final block from one iteration of DES."""
    left_side = block[:32] #first 32 bits
    print(f"Left side: {''.join(left_side)}")
    output_file.write(f"Left side: {''.join(left_side)}\n")
    right_side = block[32:] #last 32 bits
    print(f"Right side: {''.join(right_side)}")
    output_file.write(f"Right side: {''.join(right_side)}\n")
    
    k_block = key[:48] #first 48 bits
    
    new_left_side = right_side 
    new_right_side = permute(right_side, expansion_table) 
    
    print(f"Expansion permutation: {''.join(new_right_side)}")
    output_file.write(f"Expansion permutation: {''.join(new_right_side)}\n")
    
    
    
    xor_result = XOR(new_right_side, k_block)
    
    print("XOR result: ")
    output_file.write("XOR result: \n")
    
    xor_result_list = make_list_of_blocks(xor_result, 6)
    pretty_print_data(xor_result_list, 6)
    
    #There are now 8 6-bit blocks
    
    sbox_result_string = ''
    i = 0
    for block in xor_result_list:
        sbox_result_string += sbox_lookup(block, sbox_list[i])
        i += 1
        
    print(f"S-box substitution: {sbox_result_string}")
    output_file.write(f"S-box substitution: {sbox_result_string}\n")
    
    p_permutation = permute(sbox_result_string, p_table)
    
    print(f"P permutation: {''.join(p_permutation)}")
    output_file.write(f"P permutation: {''.join(p_permutation)}\n")
    
    final_right_side = XOR(p_permutation, left_side)
    
    print(f"XOR with left side: {''.join(final_right_side)}")
    output_file.write(f"XOR with left side: {''.join(final_right_side)}\n")
    
    if key == list_of_keys[-1]: #this means it's the last iteration and the sides don't need to be swapped
        whole_block = list(final_right_side) + new_left_side
        return whole_block
    
    whole_block = new_left_side + list(final_right_side)
    
    return whole_block

  
def encrypt_iterate(block, key_list):
    """Takes a 64-bit block and a list of subkeys as parameters.
        Calls the encipher_function() 16 times to permorm the 16 iterations of DES."""
    
    for i in range(16):
        print(f"iteration: {i+1}")
        output_file.write(f"iteration: {i+1}\n")
        block = encipher_function(block, key_list[i])
        
    return permute(block, ip_inverse)    

def decrypt_iterate(block, key_list):
    """Takes a 64-bit block and a list of subkeys as parameters.
        Loops throught the list of subkeys in reverse in order to decrypt the block.
        Calls the encipher_function() 16 times to permorm the 16 iterations of DES."""
    
    for i in range(15,-1,-1):
        print(f"iteration: {i+1}")
        output_file.write(f"iteration: {i+1}\n")
        block = encipher_function(block, key_list[i])
        
    return permute(block, ip_inverse)
    
    
    
def sbox_lookup(block, s_box):
    """uses the 6 bits of the block to look up the value in the s-box"""
    
    row = int(block[0] + block[5], 2) #first and last bits are the row
    column = int(block[1:5], 2) #middle 4 bits are the column
    
    digit = (s_box[row])[column]
    
    return bin(digit)[2:].zfill(4)
  
  
def XOR(string1, string2):
    """performs a bit-wise XOR on the two strings passed as parameters."""
    result = ''
    
    for i in range(len(string1)):
        if string1[i] == string2[i]:
            result += '0'
        else:
            result += '1'
    return result  


        
cwd = os.getcwd() #get the current working directory    
    
#open the output file, creating it if necessary
output_file = open(cwd + '\Python_DES\output.txt', 'w')           
    
#prompts the user to enter an 8-character key    
user_string_key = input("Enter an 8 character key: ")
print(user_string_key)

#converts the key to binary
user_string_key = key_string_to_binary(user_string_key)
print(f"The input key is: {user_string_key}")
output_file.write(f"The input key is: {user_string_key}\n")


user_string_key = list(user_string_key)

#permute the user's key by the pc1 table
user_string_key = permute(user_string_key, pc1)
  
print(f"The key after pc1: {''.join(user_string_key)}")
output_file.write(f"The key after pc1: {''.join(user_string_key)}\n")

#pass the user's permuted key and the list of keys to the subkey_generation function
#this function modifies the list that it passed to it, so no need to set the list equal to the function call
subkey_generation(user_string_key, list_of_keys)



#open the plaintext file
plaintext = open(cwd + '\Python_DES\plaintext.txt', 'r').read()
stripped_plaintext = strip_string(plaintext)
print(stripped_plaintext)

#convert the plaintext to binary
binary_string = string_to_binary(plaintext)
#user the make_list_of_blocks function to create a list of 64-bit blocks
list_of_blocks = make_list_of_blocks(binary_string, 64)

print(f"Data after preprocessing: ")
output_file.write(f"Data after preprocessing: \n")
pretty_print_data(list_of_blocks, 8)

#permute each block by the initial permutation table
list_of_blocks = permute_list_of_blocks(list_of_blocks, ip)

cipher_text = []

#encrypt every block in the list of blocks, using the same list of keys every time
for block in list_of_blocks: 
    print(f"Encypting block{list_of_blocks.index(block)+1}....")
    output_file.write(f"Encypting block{list_of_blocks.index(block)+1}....\n")
    cipher_text.append(''.join(encrypt_iterate(block, list_of_keys)))
    print(f"Final permutation: {''.join(cipher_text[list_of_blocks.index(block)])}")
    output_file.write(f"Final permutation: {''.join(cipher_text[list_of_blocks.index(block)])}\n")
    

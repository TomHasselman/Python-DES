import re #for regular expressions
import os #for finding working directory so that the path for the plaintext file can be found

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

pc2 = [14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32,
]

left_shift_list = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def string_to_binary(input_string):
    """Takes a string as input and outputs the binary representation of it.
        Represents each ASCII character as an 8-bit value"""
        
    character_list = list(input_string)
    
    return_string = ''
    
    for character in character_list:
        decimal_value = ord(character)
        binary_value = bin(decimal_value)[2:].zfill(8) # bin() prepends "0b" to the value, so slice it off. 
                                                       #Then pad with zero so that the value is 8 bits
        return_string += binary_value.rstrip()
        
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

def subkey_generation(key_string, list_to_add_to):
    key_left = key_string[:28] #first 28 bits
    key_right = key_string[28:] #last 28 bits

    for i in range(16):
        shifts = left_shift_list[i]
        
        key_left = key_left[shifts:] + key_left[:shifts] #shift left by 1
        key_right = key_right[shifts:] + key_right[:shifts] #shift left by 1
        
        list_to_add_to.append(permute(key_left + key_right, pc2))
        
        print(f"Subkey number {i+1} is: {''.join(list_to_add_to[i])}")
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

user_string = input("Enter an 8-character key: ")
print(user_string)
def generate_key(input_string):
    """Generates a 56-bit key from the 8 character input string."""
    if (len(input_string) == 8):
        binary_string = string_to_binary(input_string)
    else:
        print("Keys can only be 8 characters long.") 
        
        
user_string_key = input("Enter an 8 character key: ")
print(user_string_key)


cwd = os.getcwd() #get the current working directory


plaintext = open(cwd + '\Python_DES\plaintext.txt', 'r').read()
stripped_plaintext = strip_string(plaintext)
print(stripped_plaintext)

binary_string = string_to_binary(plaintext)

print(f"This is the first 64-bit block from the input string: {make_list_of_blocks(binary_string, 64)}")

#decimal_value = ord(character)
#binary_value = bin(decimal_value)[2:].zfill(8) #bin() prepends "0b" to the value, so slice it off. 
                                               #Then pad with zero so that the value is 8 bits

#print(f"This is the decimanl value of the character: {decimal_value}")
#print(f"This is the binary value of the character: {binary_value}")


#split 64 bit block into two 32 bit blocks
#left_side = number >> 32   #upper 32 bits
#right_side = number & 0xFFFFFFFF #lower 32 bits
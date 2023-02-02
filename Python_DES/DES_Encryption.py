import re #for regular expressions
import os #for finding working directory so that the path for the plaintext file can be found

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
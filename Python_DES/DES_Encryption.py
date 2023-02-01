import re #for regular expressions

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
        
user_string = input("Enter an ASCII String: ")
print(user_string)

#strip user_string of non-alphanumeric characters
stripped_user_string = re.sub(r'\W+', '', user_string)
print(stripped_user_string)

binary_string = string_to_binary(stripped_user_string)

print(f"This is the first 64-bit block from the input string: {make_list_of_blocks(binary_string, 64)}")

#decimal_value = ord(character)
#binary_value = bin(decimal_value)[2:].zfill(8) #bin() prepends "0b" to the value, so slice it off. 
                                               #Then pad with zero so that the value is 8 bits

#print(f"This is the decimanl value of the character: {decimal_value}")
#print(f"This is the binary value of the character: {binary_value}")


#Linux commit
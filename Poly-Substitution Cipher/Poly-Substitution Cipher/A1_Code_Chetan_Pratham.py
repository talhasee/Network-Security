import hashlib
import itertools

charsToIndc = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23, 'x':24, 'y':25, 'z':26}
indcToChar = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z'}
hexToChar = { "0": "a", "1": "b", "2": "c", "3": "d", "4": "e", "5": "f", "6": "g", "7": "h", "8": "i", "9": "j", "a": "k", "b": "l", "c": "m", "d": "n", "e": "o", "f": "p" }
charToHex = { "a": "0", "b": "1", "c": "2", "d": "3", "e": "4", "f": "5", "g": "6", "h": "7", "i": "8", "j": "9", "k": "a", "l": "b", "m": "c", "n": "d", "o": "e", "p": "f" }

def hex_to_char_mapper(hash_str):
    final_str = ""
    for i in hash_str:
        final_str += hexToChar[i]

    return final_str

def char_to_hex_mapper(char_str):
    final_str = ""
    for i in char_str:
        final_str += charToHex[i]

    return final_str

def encrypt_text(plaintext, key):

    cipher_text = ""

    hash_val = hashlib.md5(bytes(plaintext, "utf-16")).hexdigest()
    hash_in_chars = hex_to_char_mapper(hash_val)
    
    final_plaintext = plaintext + hash_in_chars
    
    for i in range(len(final_plaintext)):
        if((charsToIndc[final_plaintext[i]] + (charsToIndc[key[i%(len(key))]] - 1)) > 26):
            cipher_text += indcToChar[(charsToIndc[final_plaintext[i]] + (charsToIndc[key[i%(len(key))]] - 1))%26]
        else:
            cipher_text += indcToChar[(charsToIndc[final_plaintext[i]] + (charsToIndc[key[i%(len(key))]] - 1))]

    return cipher_text

def decrypt_text(ciphertext, key):
    decrypt_text_str = ""

    for i in range(len(ciphertext)):
        try:
            decrypt_text_str += indcToChar[(charsToIndc[ciphertext[i]] - (charsToIndc[key[i%(len(key))]] - 1))%26]
        except KeyError:
            decrypt_text_str += ciphertext[i]

    return decrypt_text_str

def check_property_text(deciphered_text):

    str_val = deciphered_text[:len(deciphered_text)-32]
    hash_val = deciphered_text[len(deciphered_text)-32:]

    final_hash_val = hashlib.md5(bytes(str_val, "utf-16")).hexdigest()
    hash_in_chars = hex_to_char_mapper(final_hash_val)

    if hash_val == hash_in_chars:
        return True
    else:
        return False

def brute_force_key(cipher_text_list):

    character_set = "abcdefghijklmnopqrstuvwxyz"

    for i in itertools.permutations(character_set, 4):
        current_key = "".join(i)
        # print(current_key)
        deciphered_text = decrypt_text(cipher_text_list[0],current_key)
        # print(deciphered_text)
        
        if (check_property_text(deciphered_text) == True):
            for i in range(1, len(cipher_text_list)):
                deciphered_text_1 = decrypt_text(cipher_text_list[i],current_key)
                
                if(check_property_text(deciphered_text_1) == False):
                    break
            else:
                return current_key

def main():
    
    key = "cbpa"

    message_list = ["hello", "world", "makes", "stairway", "heaven"]
    print("-"*32)
    print("List of plain texts")
    print(message_list)
    print("-"*32)

    encrypted_text_list = []
    
    for i in message_list:
        encrypted_text_list.append(encrypt_text(i, key))
    
    print("List of encrypted texts")
    print(encrypted_text_list)
    print("-"*32)

    print("Using bruteforce to find keys")
    key_found = brute_force_key(encrypted_text_list)
    print("-"*32)
    
    print("Key found: ", key_found)
    print("-"*32)

    
if __name__ == '__main__':
    main()

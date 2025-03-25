import numpy as np
import sys
import string

#Made by Tyler Bazemore

## matrix multiplications between the key and text is stored in list encryptedVals
def encrypt(key, text):
    
    x = np.dot(key, text)
## have to use to list as numpy uses their own array system for the output 
    encryptedVals = x.tolist()
## for loops which take the modulus of each element in list and stores it in same index in list of encryptedVals
    for ele in encryptedVals:
        encryptedVals[encryptedVals.index(ele)] = ele % 26
## with the modulus values of the matrix multiplication, use the chr() function to turn the ascii values(which is this x = num +97) into actual letters in the list, already in correct index
    for num in encryptedVals:
        x = num + 97
        encryptedVals[encryptedVals.index(num)] = chr(x)
    letters = ""
## adds the letters from the encryptedVals list to one singular string in which we can add them to the current encrypted message
    for z in encryptedVals:
        letters += z
    
    return letters


def main():
    ## all a method to read in args and convert into usable substance
    n = len(sys.argv)
    with open(sys.argv[1], 'r') as file:
        matrixDim = int(file.readline().strip('\n'))
        key = []
        for line in file.readlines():
            line = line.strip('\n')
            key.append(line.split('\t'))
    with open(sys.argv[2], 'r') as text:
        plaintext = ''
        
        for line in text.readlines():
            line = line.strip()
            line = line.lower()
            line = line.replace(" ", "")
            line = line.strip('\n')
            for char in line:
                if ord(char) < 97 or ord(char) > 122:
                    line = line.replace(char, "")
                elif char.isalpha() == False:
                    line = line.replace(char, "")
            plaintext = plaintext + line

    key = [[int(s) for s in matrixDim] for matrixDim in key]
    while len(plaintext) % matrixDim != 0:
        plaintext = plaintext + 'x'
    print("Key Matrix: ")
    for row in key:
        print("   ", *row, sep="  ")
    print("\nPlaintext:")
    print(plaintext)
    
##turns word into matrixDim size block, if matrixDim = 2 there will be 2 characters in each section
## i think this is useless as plaintextVals is dosent keep this structure but maybe its good conceptually i think
    plaintextMatrices = [(plaintext[i:i+matrixDim]) for i in range(0, len(plaintext), matrixDim)]
    

    plaintextVals = []
## turns the ascii values of each letter into 0-25 alphabet values ,via subtracting 97, in which we can use for the encryption
    for word in plaintextMatrices:
        plaintextVals.extend(ord(num)-97 for num in word)
    encryptedText = ""
## encryption begins by creating encryptedText variable than looping until all the values of the plainstext are removed from the plaintextVal
## array completeing the encrypted text message
    while len(plaintextVals) != 0:
        curEncrypt = plaintextVals[:matrixDim]
## simply set the plaintextVals to range in which we took the values to encrypt, reducing the plaintexVals list until its length is 0 breaking the loop
        plaintextVals = plaintextVals[matrixDim:]
## add output of encrypt to the total encrypted text
        encryptedText = encryptedText + encrypt(key, curEncrypt)
## ciphertext is complete Ta Da
    print("\nCiphertext:")
    print(encryptedText)
    
    
main()



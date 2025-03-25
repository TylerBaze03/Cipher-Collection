import sys

#made by Tyler Bazemore

#todo:seems finished but not getting same result as some online but it follows all the rules put out by the cipher itself


def encrypt(key, text):
    #Example keyword Fate Stay Night turns into matrix and Example text SABERW
    #|F A T E S|
    #|Y N I G H|
    #|B C D K L|
    #|M O P Q R|
    #|U V W X Z|
    retString = ""
    for i in range(len(text)):
        #set up to remove the padding letter from final string
        
        
        index = [key.index(row) for row in key if text[i][0] in row]
        index_row_1 = index[0]
        
        index = [row.index(text[i][0]) for row in key if text[i][0] in row]
        index_column_1 = index[0] 
        
        
        
        index = [key.index(row) for row in key if text[i][1] in row]
        index_row_2 = index[0] 
        
        index = [row.index(text[i][1]) for row in key if text[i][1] in row]
        index_column_2 = index[0] 
        
        
        
        #print('B4')
        #print(index_row_1, index_column_1, index_row_2, index_column_2)
        
        #same row
        if index_row_1 == index_row_2:
            if index_column_1 +1 >= 5:
                index_column_1 = 0
            else:
                index_column_1 +=1
            if index_column_2 +1 >= 5:
                index_column_2 = 0
            else:
                index_column_2 +=1
        #same column
        elif index_column_1 == index_column_2:
            if index_row_1 +1 >= 5:
                index_row_1 = 0
            else:
                index_row_1 +=1
            if index_row_2 +1 >= 5:
                index_row_2 = 0
            else:
                index_row_2 +=1
        #creating rectangle between 2 points and swapping horizontally
        #all you are doing is just swapping their column positions, very simple
        else:
            temp = index_column_1
            index_column_1 = index_column_2
            index_column_2 = temp
        
        #print('after')
        #print(index_row_1, index_column_1, index_row_2, index_column_2)
        
        
        retString = retString + key[index_row_1][index_column_1] + key[index_row_2][index_column_2]
        
            




    return retString

def createAlphaMatrix(key):
    #the mey but with duplicate letters removed
    keyStripped = ""
    retStr = [['A' for _ in range(5)] for _ in range(5) ]
    
    #False = not used True = used
    usedAscii = [False for i in range(26)]
    usedAscii[74 - 65] = True

    for letter in key:
        #all j's are turned into I regardless of key
        if letter == 'J':
            letter = 'I'
        if letter not in keyStripped:
            keyStripped = keyStripped + letter
            usedAscii[ord(letter) - 65] = True
    
    col = 0
    row = 0
    lenKey = len(keyStripped)
    keyCount = 0
    while(lenKey >0):
        while col <5:
            retStr[row][col] = keyStripped[keyCount]
            lenKey -= 1
            keyCount +=1
            col+=1
        row+=1
        col =0
    #ex string - FATESTAYNIGHT
    #becomes FATESYNIGH
    lenRemain = 25 - ((5 * row) +col)
    if lenRemain == 0:
        return retStr
    #keep going until the reamining letter(lenRemain) is equal to 0
    #check everytime what letter next needs to go in use a while loop to break early
    #possibly binary search?
    x = 0
    count = 0
    #filling rest of the matrix
    while(count < lenRemain):
        # checking if we need to move to next row
        if col >=5:
            col = 0
            row +=1
        #if used is false add it to the array at next avaible spot at than iterate column and count 
        if usedAscii[x] == False:
            retStr[row][col] = chr(x + 65)
            count += 1
            usedAscii[x] == True
            col +=1
        x +=1

    return retStr

#input 2 strings, string 1 plaintext string 2 the excryptiontext
def main():
    keyWord = ""
    plainText = ""

    #opening file and reading in plain text 
    with open(sys.argv[1], 'r') as text:
        for line in text.readlines():
            line = line.strip()
            line = line.upper()
            line = line.replace(" ", "")
            line = line.strip('\n')
            for char in line:
                if ord(char) < 65 or ord(char) > 90:
                    line = line.replace(char, "")
                elif char.isalpha() == False:
                    line = line.replace(char, "")
            plainText = plainText + line

    #opening file and reading in encryption phrase
    with open(sys.argv[2], 'r') as file:
        
        for line in file.readlines():
            line = line.strip()
            line = line.upper()
            line = line.replace(" ", "")
            line = line.strip('\n')
            for char in line:
                if ord(char) < 65 or ord(char) > 90:
                    line = line.replace(char, "")
                elif char.isalpha() == False:
                    line = line.replace(char, "")
            keyWord = keyWord + line
    keyCiphStr = createAlphaMatrix(keyWord)
    
    for i in range(1, len(plainText),1):
        if plainText[i-1] == plainText[i]:
            print(plainText[:i] + "123" + plainText[i:])
            plainText= plainText[:i] + 'X' + plainText[i:]

    if (len(plainText) % 2 !=0):
        plainText += 'X'

    #will always be even after padding
    plainTextDuple = [['A' for _ in range(2)] for _ in range(int(len(plainText)/2)) ]
    
    
    ptRow = 0
    ptCol = 0
    
    #skipping letters
    for j in range(len(plainText)):
        #print(plainText[j], ptRow, ptCol)
        if ptCol < 2:
            #print('Y')
            plainTextDuple[ptRow][ptCol] = plainText[j]
            
            ptCol+=1

        else:
            #print("n")
            ptCol = 0
            ptRow+=1
            plainTextDuple[ptRow][ptCol] = plainText[j]
            ptCol +=1
    
    print(plainText)
    print(plainTextDuple)
    
    encryptedStr = encrypt(keyCiphStr, plainTextDuple)

    print(encryptedStr)


    return 0

main()
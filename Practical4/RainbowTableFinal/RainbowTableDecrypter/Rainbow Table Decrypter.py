#Rainbow Table Decrypter 

import random
import hashlib
import csv
import sympy
import pandas as pd
import time 

lettersLowerDict = 'abcdefghijklmnopqrstuvwxyz'
lettersUpperDict = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbersDict = str("0123456789")

chainLink = ""
hashedChainLink = ""
pwSpaceSize = 0
currentLink = 0
duplicatClearAttempts = 0


############ Decrypter Settings ############

#Type of Input
#0 = will not be included, 1 = will be included 

print('Add numbers to dictionary? 1=yes 0=no:')
#numbers = input()
numbers = 1

print('Add lowercase alphabet to dictionary? 1=yes 0=no:')
#alphabetLowerCase = input()
alphabetLowerCase = 0

print('Add uppercase alphabet to dictionary? 1=yes 0=no:')
#alphabetUpperCase = input()
alphabetUpperCase = 0

fullDictionary = "" #if you want any unique charecters, add them here

#Length of Password

print('password length?: ')
#passwordLength = input()
passwordLength = 8

#Length of Rainbow Table

print('Rainbow Table Length?: ')
#rainbowTableLength = input()                                #8 chars                                #8chars                                                                     # 6  chars
rainbowTableLength = 57778   # (111111110 * 1.3) / 2500 = 57778       # if chain length = 5000 (4999) then (111111110 * 1.3) / 5000 = 28889  # (1111110 * 1.3) / 2500 = 578
                                                                                                                                           

#Length of Chains
print('Chain Length?: ')
#chainLength = input()  
chainLength = 2499 #starts at 0, so real length is this value + 1 #was at 2499  

#Hash to be decrypted

print('Hash to decrypt?: ')
#hashToDecrypt = input()  
hashToDecrypt = "d21adcdf0b81bc69bff6e106a52c763c0812232c"

#############################################

#Constructs the full dictionary of charecters used from your selection

if(numbers == 1):
    fullDictionary = fullDictionary + numbersDict

if(alphabetLowerCase == 1):
    fullDictionary = fullDictionary + lettersLowerDict

if(alphabetUpperCase  == 1):
    fullDictionary = fullDictionary + lettersUpperDict


#print(fullDictionary)

#Contains the reduction functions

def Reduction_Function_Numeric():
    NumericAscii = Map_Ascii_To_Number()
    passwordSpace = Password_Space_Size_Calculator()
    chainLink = ""
    z = passwordLength

    while (z > 0):
        r = NumericAscii % len(fullDictionary)
        NumericAscii = NumericAscii // len(fullDictionary)
        chainLink = fullDictionary[r] + chainLink
        NumericAscii - NumericAscii - 1
        NumericAscii = NumericAscii
        z -= 1
        
        #charValueHolder = (remainingPasswordSpace) % 11  #For a 25 char dictionary, this is 27 to allow 0 = nothing, easily making variable string size possible
       # remainingPasswordSpace = remainingPasswordSpace / 11 
      #  chainLink = chainLink + Dictionary_Map(charValueHolder)
    
    #chainLink.strip()

    return chainLink

#Contains the hashing algorithm

def SHA1_Hash(chainLink):
    hashedChainLink = ""

    encoded_string = chainLink.encode()
    hash_object = hashlib.sha1(encoded_string)
    hashedChainLink = hash_object.hexdigest()
    
    return hashedChainLink

#Calculates the size of the password space

def Password_Space_Size_Calculator():
    passwordSpaceSize = 0
    iterator = 0
    for x in range(passwordLength):
        passwordSpaceSize = passwordSpaceSize + (len(fullDictionary) ** (passwordLength - iterator))
        iterator += 1 
    
    return passwordSpaceSize 

#Converts the hash into its ascii value, then into a value that can be converted back into plain text

def Map_Ascii_To_Number():
    #asciiNumValue = sum(bytearray(hashedChainLink, "utf8"))
    asciiNumValue = (int(hashedChainLink, 16) + currentLink)
    nextPrimeNumber = sympy.nextprime(Password_Space_Size_Calculator())  
    asciiNumValue = asciiNumValue % nextPrimeNumber

    return asciiNumValue



######################## Main Body of the Program ############################## 

####################### Initial Table Generation ############################## 
start_time = time.time()


chainData = []
chainIndex = []
chainEndsToCompare = []
z = 0
p = 0
noOfChainAttempts = 0


while(p <= ((chainLength*2)+1)): 
    p += 1 
    chainIndex.append(p)


with open('RainbowTableLookUpTable.csv', 'a+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(chainIndex)



while (z <= chainLength):
    noOfChainAttempts = noOfChainAttempts + 1
    chainData = []
    chainLink = hashToDecrypt
    currentLink = 0 + z
    chainData.insert(0, chainLink)
    hashedChainLink = hashToDecrypt
    y = 0 

    while (y <= (chainLength) - z):

        chainLink = Reduction_Function_Numeric()
        chainData.insert(0, chainLink)

        hashedChainLink = SHA1_Hash(chainLink)
        chainData.insert(0, hashedChainLink)

        currentLink += 1
        y += 1

    chainEndsToCompare.insert(0, chainLink)
    with open('RainbowTableLookUpTable.csv', 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(chainData)
        
    print ("Chain: " + str(z + 1) + " of " + str((chainLength + 1)) + " Completed ")
    z += 1
    

print("\nRainbow Table Look Up Table Completed in:  ""--- %s seconds ---" % (time.time() - start_time) + "\n")



####################### Check table for end chains  ############################## 

df = pd.read_csv ('RainbowTable.csv')
lookupAttempt = 0
endChainComparison = []
finalChainExpanded = []
while(lookupAttempt < len(chainEndsToCompare)):
    endChainComparison = df.loc[df['Chain End']==chainEndsToCompare[lookupAttempt]]
    
    if(endChainComparison.empty != True):
        break
    else:
        lookupAttempt += 1


if(endChainComparison.empty == True):
    pass
else:
    chainLink = endChainComparison[0]


currentLink = 0 
while((hashedChainLink != hashToDecrypt) and (currentLink < (chainLength+1))):

    hashedChainLink = SHA1_Hash(chainLink)
    finalChainExpanded.insert(0, hashedChainLink)

    chainLink = Reduction_Function_Numeric()
    finalChainExpanded.insert(0, chainLink)

    currentLink += 1

valueToPrint = ((currentLink*2) - (len(finalChainExpanded)))
print("Value Decrypted: " + finalChainExpanded[valueToPrint]) 
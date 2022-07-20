#Rainbow Table Generator

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


############ Generator Settings ############

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
#rainbowTableLength = input()                                                                                                   # 6  chars
rainbowTableLength = 57778   
                                                                                                                                           

#Length of Chains

print('Chain Length?: ')
chainLength = input()  
chainLength = 2499 #starts at 0, so real length is this value + 1 #was at 2499  

#############################################

#Constructs the full dictionary of charecters used from your selection

if(numbers == 1):
    fullDictionary = fullDictionary + numbersDict

if(alphabetLowerCase == 1):
    fullDictionary = fullDictionary + lettersLowerDict

if(alphabetUpperCase  == 1):
    fullDictionary = fullDictionary + lettersUpperDict


#Contains the reduction functions

def Reduction_Function_Numeric():
    NumericAscii = Map_Ascii_To_Number()
    chainLink = ""
    z = passwordLength

    while (z > 0):
        r = NumericAscii % len(fullDictionary)
        NumericAscii = NumericAscii // len(fullDictionary)
        chainLink = fullDictionary[r] + chainLink
        NumericAscii - NumericAscii - 1
        NumericAscii = NumericAscii
        z -= 1

    return chainLink

#Contains the hashing algorithm

def SHA1_Hash(chainLink):
    hashedChainLink = ""

    encoded_string = chainLink.encode()
    hash_object = hashlib.sha1(encoded_string)
    hashedChainLink = hash_object.hexdigest()
    
    return hashedChainLink

#Generates a random string to start the chain

def Chain_Starter(chainLink):
    chainLink = ""
    for x in range(passwordLength):
        chainSelector = random.randint(0,(len(fullDictionary)))
        if(chainSelector == len(fullDictionary)):
            pass
        else:
            chainLink = chainLink + fullDictionary[chainSelector]

    return chainLink

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
    asciiNumValue = (int(hashedChainLink, 16) + currentLink)
    nextPrimeNumber = sympy.nextprime(Password_Space_Size_Calculator())  
    asciiNumValue = asciiNumValue % nextPrimeNumber

    return asciiNumValue

#Takes the csv, removes duplicates, records the amount of duplicates, then generates that many amount of new chains 

def Duplicate_Cleaner():

    numOfDuplicates = 0
    
    data = pd.read_csv('RainbowTable.csv')

    data.drop_duplicates(subset =["Chain End"], keep = 'first', inplace = True) 
    data.to_csv('RainbowTable.csv', index=False)


    file = open("RainbowTable.csv")
    reader = csv.reader(file)
    numOfDuplicates = (rainbowTableLength - len(list(reader)))

    return numOfDuplicates



######################## Main Body of the Program ############################## 

####################### Initial Table Generation ############################## 
start_time = time.time()


chainData = ["thisisempty",'thisisempty']
z = 0
noOfChainAttempts = 0

with open('RainbowTable.csv', 'a+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Chain Start" , "Chain End"])
        

while (z <= rainbowTableLength):
    noOfChainAttempts = noOfChainAttempts + 1

    chainLink = Chain_Starter(chainLink)
    currentLink = 0
    chainData[0] = chainLink

    for y in range(chainLength):
        hashedChainLink = SHA1_Hash(chainLink)
        chainLink = Reduction_Function_Numeric()

        currentLink += 1
        
        if (chainLink == ""):
            break

    if (chainLink == ""): 
       pass 

    else:
        chainData[1] = chainLink
        with open('RainbowTable.csv', 'a+', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(chainData)
        
        print ("Chain: " + str(z + 1) + " of " + str(rainbowTableLength) + " Completed ")
        z += 1


######################## Duplicate removal and replacement Generation ############################## 

numOfDuplicates = Duplicate_Cleaner()


while (numOfDuplicates > 0): #  and duplicatClearAttempts < 100
    duplicatClearAttempts += 1
    print("Clearing Duplicates Attempt: " + str(duplicatClearAttempts))
    z = 0
    noOfChainAttempts = 0
            
    while (z < numOfDuplicates):
        noOfChainAttempts = noOfChainAttempts + 1

        chainLink = Chain_Starter(chainLink)
        currentLink = 0
        chainData[0] = chainLink

        for y in range(chainLength):
            hashedChainLink = SHA1_Hash(chainLink)
            chainLink = Reduction_Function_Numeric()

            currentLink += 1
            
            if (chainLink == ""):
                break

        if (chainLink == ""): 
            pass 

        else:
            chainData[1] = chainLink
            with open('RainbowTable.csv', 'a+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(chainData)
            
            print ("Duplicate Chain: " + str(z + 1) + " of " + str(numOfDuplicates) + " Replaced")
            z += 1
    
    
    numOfDuplicates = Duplicate_Cleaner()
 

print("\nRainbow Table Completed in:  ""--- %s seconds ---" % (time.time() - start_time) + "\n")

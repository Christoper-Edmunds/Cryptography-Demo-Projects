
#BruteForceDecrypter
from ast import If
import hashlib
import itertools
import time

userInput = ""
encryptionOuput = ""
hash1List = ""
dictionary = "0123456789qwertyuiopasdfghjklzxcvbnm"
passwordSpace = 2176782336
x = 0
potentialString = ""


def Sha1_Encryption(potentialString):
    encryptionInput = ""
    encryptionInput = hashlib.sha1(potentialString.encode())
    encryptionOuput = encryptionInput.hexdigest()

    return encryptionOuput 

print ("Enter 1 to encrypt SHA1, Enter 2 to decrypt (brute force) SHA1")
menuInput = input()
if (menuInput == "1"):

    print("Enter String to encrypt with SHA1: ")
    userInput = input()
    encryptionOuput = hashlib.sha1(userInput.encode())
    print ("Your SHA1 hash is " + encryptionOuput.hexdigest())

else:

    print("Hash set A or B? A: SHA1  B:BCH10,6")
    hashChoice = input()

    if (hashChoice == "A" or hashChoice == "a"):
    
        print("Enter HASH to decrypt: ")
        userInput = input()

        start_time = time.time()

        ##########main body############
        for i in itertools.product(["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], repeat=6):
            potentialString = ''.join(i)
            encryptionOuput = Sha1_Encryption(potentialString)

            if (encryptionOuput == userInput):
                hashFound = True
                break 
        
        print("Decrypted String: " + potentialString)

        print("\nCompleted in:  ""--- %s seconds ---" % (time.time() - start_time) + "\n")
    else:

        print("Enter HASH to decrypt: ")
        userInput = input()   
        start_time = time.time()

        ##########main body############
        for i in itertools.product(["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], repeat=10):
            potentialString = ''.join(i)
            encryptionOuput = Sha1_Encryption(potentialString)

            if (encryptionOuput == userInput):
                hashFound = True
                break 

        print("Decrypted String: " + potentialString)

        print("\nCompleted in:  ""--- %s seconds ---" % (time.time() - start_time) + "\n")
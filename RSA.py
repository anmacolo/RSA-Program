import random
def Convert_Num(_list):
    _string = ''
    for i in _list:
        _string += chr(i)
    return _string

def Find_Bezout_1(a,b):
    s1, t1 = 1, 0 #initial coefficients for a: a = a*1 + b*0
    s2, t2 = 0, 1
    
    while (b>0): #loop ends when b reaches 0
        k = a % b
        quotient = a // b
        
        a = b
        b = k
        
        new_s1, new_t1 = s2, t2 #used to update s1, t1 later
        new_s2, new_t2 = s1 - quotient * s2, t1 - quotient * t2 #used to update s2, t2 later
        
        s1, t1 = new_s1, new_t1
        s2, t2 = new_s2, new_t2
        
    return s1 #returns first Bezout coefficient

def Find_Bezout_2(a,b):
    s1, t1 = 1, 0 #initial coefficients for a: a = a*1 + b*0
    s2, t2 = 0, 1 #initial coefficients for b: b = a*0 + b*1
    
    while (b>0):
        k = a % b
        quotient = a // b
        
        a = b
        b = k
        
        new_s1, new_t1 = s2, t2
        new_s2, new_t2 = s1 - quotient * s2, t1 - quotient * t2
        
        s1, t1 = new_s1, new_t1
        s2, t2 = new_s2, new_t2
        
    return t1 #returns second Bezout coefficient

    
def Find_Private_Key_d(e, p, q):
    relatively_prime_to_e = ((p-1)*(q-1))
    if Euclidean_Alg(Bezout_1 * e,relatively_prime_to_e) == 1:
        d = Bezout_1
    else:
        d = Bezout_2
    if d < 0:
        d = d + (relatively_prime_to_e)
    return d

def FME(b, n, m):
    result = 1 #initializes result
    square = b #initializing the variable square with the value of b
    while (n>0): #while loop: loop stops when n reaches 0
        r = n % 2 #provides value of n mod 2
        n = n // 2 #integer division, converting n to binary
                     
        if r == 1: #acculumates 1 bits in binary expansion
            result = (result * square) % m #updating the value of result at each step
     
        square = (square * square) % m #updating the value of square at each step
    return result #returns final value of result once n is no longer greater than 0

def Euclidean_Alg(a, b): #EEA called again to return GCD only, no Bezout coefficients
    s1, t1 = 1, 0 #initial coefficients for a: a = a*1 + b*0
    s2, t2 = 0, 1 #initial coefficients for b: b = a*0 + b*1
    
    while (b>0): #loop ends when b reaches 0
        k = a % b #mod operation: used to update b at each step
        quotient = a // b #quotient used to update s2, t2
        
        a = b #update value of a
        b = k #update value of b
        
        new_s1, new_t1 = s2, t2 #used to update s1, t1 later
        new_s2, new_t2 = s1 - quotient * s2, t1 - quotient * t2 #used to update s2, t2 later
        
        s1, t1 = new_s1, new_t1 #s1 and t1 updated
        s2, t2 = new_s2, new_t2 #s2 and t2 updated
        
    return a

def Find_Public_Key_e(p, q): #include check so e doesn't equal p or q
    n = (p)*(q)
    relatively_prime_to_e = (p-1)*(q-1)
    
    while True: #while loop, runs until loop is broken
        e = random.randint(1,1000) #generates random integer
        if (Euclidean_Alg(e, relatively_prime_to_e) == 1): #tests if variables are relatively prime
            break #ends while loop
    
    return e

def Convert_Text(_string):
    integer_list = []
    for letter in _string:
        integer_list.append(ord(letter))
    return integer_list

def Encode(n, e, message):
    conversion = Convert_Text(message)
    cipher_text = []
    for numbers in conversion:
        cipher_text.append(FME(numbers, e, n))
    
    return cipher_text

def Decode(n, d, cipher_text):
    message = ''
    decoded_nums = []
    for numbers in cipher_text:
        decoded_nums.append(FME(numbers, d, n))
    message = Convert_Num(decoded_nums)
    
    return message

shutdown = False
while(shutdown == False): #while loop runs until user quits
    answer = str(input("Encode or Decode a message? (Enter Encode or Decode or Q to quit)"))
    if answer.strip().lower() == "encode":
        message = str(input("Please enter a message to be encoded:")) #user enters a string
        unencrypted_message = Convert_Text(message) #Unencrypted message
        print("Your unencrypted message is: {}".format(unencrypted_message))
        
    
        p = int(input("Please enter a prime number:"))
        q = int(input("Please enter another prime number:"))
        n = p*q #p and q are prime factors
        answer2 = int(input("Press 1 to generate a random public key, press 2 to enter a public key"))
        if answer2 == 1:
            e = Find_Public_Key_e(p,q) #generates a public key e
        if answer2 == 2:#use to encode messages for code breaking with pre-existing e
            e = int(input("Please enter the value of your public key")) #should only be used if e is already provided
        relatively_prime_to_e = (p-1)*(q-1)
        Bezout_1 = Find_Bezout_1(e,relatively_prime_to_e)
        Bezout_2 = Find_Bezout_2(e,relatively_prime_to_e)
        d = Find_Private_Key_d(e,p,q) #generates private key d (finds modular inverse)


        print("Your public key (n, e) is: ({}, {})".format(n,e)) #prints public keys
        print("Your private key (n, d) is: ({}, {})".format(n,d)) #prints private keys
        encoded_message = Encode(n, e, message) #encodes message
        print("Your encoded message is: {}".format(encoded_message))

    elif answer.strip().lower() == "decode":
        encoded_nums = str(input("Please enter encoded numbers separated by commas (exclude brackets)")) #numbers are entered as strings
        nums_only = encoded_nums.split(",") #removes commas from the string, only numbers remain
        encoded_list = []
        for nums in nums_only:
            encoded_list.append(int(nums)) #string values are converted to integers and appended to list
        n = int(input("Please enter Private Key n"))
        d = int(input("Please enter Private Key d"))
        decoded_message = Decode(n,d,encoded_list)
        print("The decoded message is: {}".format(decoded_message))
    elif answer == "Q":
        shutdown = True #user has quit, while loop breaks
        print("Have a nice day!")
    else:
        print("Please enter Encode or Decode")

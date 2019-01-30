
def caesar(text,shift,**kwargs): # shift = int
    if kwargs.get("decode",False):
        shift =  shift*-1
    newText = ""
    alpha = "abcdefghijklmnopqrstuvwxyz"

    for eachletter in text:
        if eachletter.lower() not in alpha:
            newText += eachletter

        elif eachletter in alpha:
            index = (alpha.find(eachletter)+shift) % len(alpha)
            newText += alpha[index]

        else:
            index = (alpha.find(eachletter.lower())+shift) % len(alpha)
            newText += alpha[index].upper()

    return newText

def xorcipher(text, key, **kwargs): # key = string of length 1 mixing xor with other encryption screws up decoding

    newText = ""
    for char in text:
        newText += chr(ord(char) ^ ord(key))

    return newText

def keywordencrypt(text, key): #key = string

    newText = ""
    alpha = "abcdefghijklmnopqrstuvwxyz"
    table = key

    for char in alpha:
        if char not in key:
            table += char

    for char in text:
        if char not in table:
            newText += char

        elif char in table:
            index = alpha.find(char)
            newText += table[index]

        else:
            index = alpha.find(char)
            newText += table[index].upper()


    return newText


def keyworddecrypt(text, key):
    newText = ""
    alpha = "abcdefghijklmnopqrstuvwxyz"
    table = key

    for char in alpha:
        if char not in key:
            table += char

    for char in text:
        if char not in table:
            newText += char

        elif char in table:
            index = table.find(char)
            newText += alpha[index]

        else:
            index = table.find(char)
            newText += alpha[index].upper()

    return newText

def keywordcipher(text, key, **kwargs):
    if kwargs.get("decode", False):
        return keyworddecrypt(text, key)
    else:
        return keywordencrypt(text, key)


def railfence(plainText,num_of_rails): # key = int

    try:
        plainText = plainText.replace(" ", "")
    except:
        pass
    if num_of_rails == 1:
        rails = [[] for i in range(num_of_rails+1)]
    else:
        rails = [[] for i in range(num_of_rails)]
        num_of_rails -= 1

    invert = False
    counter = -1
    for eachletter in plainText:
        counter += 1
        if counter <= num_of_rails and not invert:
            rails[counter].append(eachletter)

        elif counter <= num_of_rails and invert:
            rails[num_of_rails - counter].append(eachletter)

        if counter == num_of_rails:
            invert = not invert
            counter = 0

    return [char for rail in rails for char in rail]

def railfence_encode(plainText,num_of_rails):

    return ''.join(railfence(plainText,num_of_rails))


def railfence_decode(encText,num_of_rails):
    char_pos = list(range(len(encText)))
    correct_pos = railfence(char_pos,num_of_rails)

    return ''.join(encText[correct_pos.index(pos)] for pos in char_pos)

def railfence_handler(plainText, num_of_rails, **kwargs):
    if kwargs.get("decode",False):
        return railfence_encode(plainText,num_of_rails)
    else:
        return railfence_decode(plainText,num_of_rails)
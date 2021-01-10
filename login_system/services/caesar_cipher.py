import random

numbers = "1234567890ζαΔδξ¤¥֏௹₡฿₢₣₩₱₳"
symbols = "&?.,!@#$%;:_+=-*()~^<>}{[]"

alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
space = " "
other_symbols = list("₼ϟϙͲ")
selected = random.choice(other_symbols)


def cipher_text(text, key):
    """ Generates a ciphered text from the text using the Caesar Cipher algorithm

    :param text: Text to be ciphered
    :type text: str
    :param key: the key used to cipher the text *required*
    :type key: int
    :return: a ciphered text
    :rtype: str
    """

    ciphered_text = ""
    try:
        for letter in text:
            if letter in alphabets:
                letter_position = alphabets.index(letter)
                new_letter = alphabets[(letter_position + key) % len(alphabets)]
                ciphered_text += new_letter

            elif letter in numbers:
                number_position = numbers.index(letter)
                new_symbol = symbols[(number_position + key) % len(symbols)]
                ciphered_text += new_symbol

            elif letter in symbols:
                symbol_position = symbols.index(letter)
                new_number = numbers[(symbol_position + key) % len(numbers)]
                ciphered_text += new_number

            elif letter in space:
                new_space = random.choice(other_symbols)
                ciphered_text += new_space
            else:
                ciphered_text += letter
        return ciphered_text
    except:
        raise


def decipher_text(text, key):
    """ Decipheres a string ciphered with Caesar Cipher algorithm

    :param text: text to be deciphered
    :type text: str
    :param key: key used to cipher the text. *required* 
    :type key: int
    :return: plain text
    :rtype: str
    """
    deciphered_text = ""
    try:
        for letter in text:
            if letter in alphabets:
                letter_position = alphabets.index(letter)
                new_letter = alphabets[(letter_position - key) % len(alphabets)]
                deciphered_text += new_letter

            elif letter in numbers:
                number_position = numbers.index(letter)
                new_symbol = symbols[(number_position - key) % len(symbols)]
                deciphered_text += new_symbol

            elif letter in symbols:
                symbol_position = symbols.index(letter)
                new_number = numbers[(symbol_position - key) % len(numbers)]
                deciphered_text += new_number

            elif letter in other_symbols:
                old_space = space[0]
                deciphered_text += old_space
            else:
                deciphered_text += letter
        return deciphered_text
    except:
        raise


if __name__ == '__main__':
    while 1:
        message = input("Message: ")
        key = int(input("Key: "))
        ciphered_text = cipher_text(message, key)
        deciphered_text = decipher_text(ciphered_text, key)
        print("\n")
        print(f"Ciphered Text: {ciphered_text}")
        print(f"Deciphered Text: {deciphered_text}")
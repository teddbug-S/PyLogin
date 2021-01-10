from pprint import pprint
from math import ceil


def cipher_text(text, key):
    """ Ciphers a text using the transposition cipher algorithm

    :param text: text to be ciphered
    :type text: str
    :param key: cipher key
    :type key: int
    """
    
    def get_table():
        """ Generates the cipher table """
        table, index = [], 0
        while index < len(text):
            row = []
            while len(row) < key:
                if index == len(text): # if the text gets finished and our row is incomplete
                    row.append('') # we add empty qoutes
                else:
                    row.append(text[index])
                    index += 1
            table.append(row)
        # pprint(table)
        return table
    
    def get_ciphered_text() -> str:
        """ Extract the letters from the cipher table

        :return: ciphered_text
        :rtype: str
        """
        table, ciphered_text = get_table(), ""
        ciphered_text = ''.join([letter for index in range(key) for row in table for letter in row[index]])
        return ciphered_text


    return get_ciphered_text()



def decipher_text(text, key):
    """ Deciphers text ciphered using the transposition cipher algorithm

    :param text: ciphered text
    :type text: str
    :param key: key used to cipher text
    :type key: int
    """
    
    def get_table():
        """ Generates the decipher table

        :return: table
        :rtype: list
        """
        table, index = [], 0 # initialize the table and index
        row_num = ceil((text_length := len(text))/key) # number of each row
        exclude_cell = key*row_num-text_length # cells to shade out or exclude
        while len(table) < key: # number of rows
            row = []
            while len(row) < row_num: # number of columns
                if index >= text_length: # if we are at the end of the text and row not full,
                    row.append('') # we add space
                else:
                    row.append(text[index]) # we continue
                index += 1
            table.append(row) # append to table
            if key-len(table) == exclude_cell: # 
                row_num -= 1
        return table

    
    def get_deciphered_text() -> str:
        """ Extracts the ciphered text from the table cipher table

        :return: the deciphered or plain text
        :rtype: str
        """
        plain_text = ""
        table = get_table()
        row_num = ceil(len(text)/key)
        for index in range(row_num):
           for row in table:
               if index >= len(row):
                   continue
               plain_text += row[index]

        return plain_text


    return get_deciphered_text()



if __name__ == '__main__':
    while 1:
        message = input("Message: ")
        key = int(input("Key: "))
        ciphered_text = cipher_text(message, key)
        deciphered_text = decipher_text(ciphered_text, key)
        print("\n")
        print(f"Ciphered Text: {ciphered_text}")
        print(f"Deciphered Text: {deciphered_text}")
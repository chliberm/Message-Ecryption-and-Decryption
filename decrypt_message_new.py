"""
Celia Liberman
CS 021 Final Project
This program accepts two text files of a key and a encrypted message both in
matrix form and decodes it and returns the decrypted message to the user
"""


# import numpy
import numpy as np


# define two lists as constants, alphabet and list of corresponding numbers
CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
              'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', 'A',
              'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
              'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', ',', "'",
              '!', '?']
NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
           21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
           39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
           57, 58]


def main():
    # get input for the file name of the key file 
    key_file = input("Enter the name with extension of the file containing the key: ")
    # convert the key matrix to 2D lists
    key, num_rows = get_matrix(key_file)
    # make sure the file exist and prompt user to enter again if it doesn't
    while key == False:
        print("Error: Key file could not be found")
        key_file = input("Enter the name with extension of the file containing the key: ")
        key, num_rows = get_matrix(key_file)
    # get the inverse of the key matrix and check invertibility 
    inv_key, invert = get_inverse(key)
    while invert == False:
        print('Error: Matrix not invertible.')
        # get input for name of txt file containing the key matrix
        key_file = input("Enter the name of the file containing an invertible key matrix: ")
        # get key as 2D list and number of rows using the get_key_matrix function
        key, num_rows = get_matrix(key_file)
        # make sure file exists
        while key == False:
            print("Error: Key file could not be found")
            key_file = input("Enter the name with extension of the file containing the key: ")
            key, num_rows = get_matrix(key_file)
        # get the inverse of the key matrix
        inv_key, invert = get_inverse(key)

    # get input for the file name of the encrypted message file
    encr_msg_file = input("Enter the name with extension of the file containing the encrypted "
                          + "message: ")
    # convert the encrypted message matrix to 2D list
    encr_msg, num_rows = get_matrix(encr_msg_file)
    # make sure the file exist and prompt user to enter again if it doesn't
    while encr_msg == False:
        print("Error: Encrypted message file could not be found")
        encr_msg_file = input("Enter the name with extension of the file containing the encrypted "
                          + "message: ")
        encr_msg, num_rows = get_matrix(encr_msg_file)
        
    # get column length
    col_nums = len(encr_msg[0])
    # multiply the inverse of the key and the encrypted message to get the decrypted
    # matrix
    try:
        decr_msg = get_decrypted_message(inv_key, encr_msg, num_rows, col_nums)
    except IndexError:
        print('Error: Incorrect key or encrypted message. Could not preform matrix multiplication')
    else:
        # convert the decrypted matrix to a string of letter to form the final decrypted
        # message
        final_msg, decodability = decipher_message(decr_msg)
        if decodability == False:
            print('Error: decoded matrix not decipherable')
        else:
            # ask user if they want to display the message here or create a file with the message
            response = input('Would you like to display the final message here or create a text file '
                            + 'of the message? Type "display" or "file": ')
            while response != 'display' and response != 'file':
                print("Invalid input. Try again.")
                response = input('Would you like to display the final message here or create a text file '
                            + 'of the message? Type "display" or "file": ')
            if response == 'display':
                print(final_msg)
            elif response == 'file':
                file_name = input('Enter the desired name of the file with extension: ')
                msg_file = open(file_name, 'w')
                msg_file.write(final_msg)
                msg_file.close()


def get_matrix(file_name):
    """ Receive a file name and reads a txt file with a matrix and turns it into
    a 2D list of the rows of the matrix (formed as lists as well) while converting
    the string of numbers to integers. Also is case insensitive. Return a final
    2D list and the number of rows"""
    try:
        matrix_file = open(file_name, 'r')
    except IOError:
        return False, False
    else:
        line = matrix_file.readline()
        matrix = []
        while line:
            line = line.rstrip()
            line_split = line.split()
            for num in line_split:
                number = int(num)
                try:
                    num_index = line_split.index(num)
                except ValueError:
                    print('Error: item could not be found')
                else:
                    line_split[num_index] = number
            matrix.append(line_split)
            line = matrix_file.readline()
        matrix_file.close()

        return matrix, len(matrix)


def get_inverse(matrix):
    """ Receives a 2D list as a matrix and preforms an inverse operation
    """
    try:
        matrix = np.array(matrix)
        m_inv = np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        return 0, False
    else:
        return m_inv, True


def get_decrypted_message(inverse, message, row_num, col_num):
    """ Receives two 2D list as arguments as well as number of rows and number of
    columns and preforms matrix multiplication on the two lists to create a final
    matrix of the decrypted message. Returns a 2D list"""
    decrypted_msg = []
    for n in range(0, row_num):
        row = []
        for col_index in range(0, col_num):
            total = 0
            element = 0
            for row_index in range(0, row_num):
                total += message[row_index][col_index] * inverse[n][row_index]
            element += total
            row += [element]
        decrypted_msg += [row]
    
    return decrypted_msg


def decipher_message(message):
    """ Receives a 2D list as an argument and converts it to a
    2D list that represents the message. Returns a 2D list of alphabetical characters"""
    message_str = ''
    for lst in message:
        line = ''
        for num in lst:
            try:
                num_index = NUMBERS.index(num)
            except ValueError:
                message_decode = False
            else:
                ch = CHARACTERS[num_index]
                line += ch
                message_decode = True
        message_str += line
    return message_str, message_decode
                    

# call main
main()

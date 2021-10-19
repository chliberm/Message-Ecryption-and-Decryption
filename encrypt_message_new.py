"""
Celia Liberman
CS 021 Final Project
This program accepts a message from the user and decrypts it based on a key in
form of a matrix using matrix multiplication and the conversion of the message
to a matrix of corresponding numbers
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
    # get input for name of txt file containing the key matrix
    key_file = input("Enter the name with extension of the file containing the key: ")
    # get key as 2D list and number of rows using the get_key_matrix function
    key, num_rows = get_matrix(key_file)

    # make sure file exists
    while key == False:
        print("Error: Key file could not be found")
        key_file = input("Enter the name with extension of the file containing the key: ")
        key, num_rows = get_matrix(key_file)

    # check key matrix invertibility
    key_inv = check_invertibility(key)
    # make sure key is invertible
    while key_inv == False:
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
        # check key matrix invertibility
        key_inv = check_invertibility(key)

    # get input for message to be encrypted
    message = input("Enter the message to be encrypted (use only alphabetical letters and "
                    + "limit symbols to . , ! ?): ")

    # get matrix as 2D list and number of columns using get_message_matrix
    msg_matrix, num_columns = get_message_matrix(message, num_rows)
    while msg_matrix == False:
        # get input for message to be encrypted
        message = input("Enter the message to be encrypted (use only alphabetical letters and "
                        + "limit symbols to . , ! ?): ")

        # get matrix as 2D list and number of columns using get_message_matrix
        msg_matrix, num_columns = get_message_matrix(message, num_rows)
    # encrypt the message matrix using get_encrypted_message
    msg_encr = get_encrypted_message(key, msg_matrix, num_rows, num_columns)
    # receive name of new file to created with encrypted message matrix
    encr_file_name = input("Enter the name desired for the encrypted matrix text file "
                           + "(include extension): ")
    # open new to write the encrypted message to
    encrypt_msg_file = open(encr_file_name, 'w')
    # convert 2D list of encrypted message to lines of strings and write in new file
    message_lst = convert_2D_list(msg_encr)
    for line in message_lst:
        encrypt_msg_file.write(line)
    encrypt_msg_file.close()
    print("Congrats! You're very secret message has been successfully encrypted.")
    print("A file was created with the encrypted matrix called '", encr_file_name, "'.")


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


def get_message_matrix(message, rows_num):
    """ Receives a string and numbers of rows as arguments and converts it to a
    2D list that represents the message matrix with number of rows based on the
    key. Returns a 2D list and number of columns"""
    message_lst = list(message)
    message_nums = []
    for ch in message_lst:
        try:
            ch_index = CHARACTERS.index(ch)
        except ValueError:
            print('Error: message contains non-usable characters')
            return 0, 0
        else:
            ch_num = NUMBERS[ch_index]
            message_nums += [ch_num]
    while len(message_nums) % rows_num != 0:
        message_nums += [27]
    columns_num = len(message_nums) // rows_num
    matrix_msg = []
    while message_nums != []:
        row = message_nums[0:columns_num]
        for item in row:
            message_nums.remove(item)
        matrix_msg += [row]

    return matrix_msg, columns_num


def get_encrypted_message(key, message, row_num, col_num):
    """ Receives two 2D list as arguments as well as number of rows and number of
    columns and preforms matrix multiplication on the two lists to create a final
    matrix of the encrypted message. Returns a 2D list"""
    encrypted_msg = []
    for n in range(0, row_num):
        row = []
        for col_index in range(0, col_num):
            total = 0
            element = 0
            for row_index in range(0, row_num):
                total += message[row_index][col_index] * key[n][row_index]
            element += total
            row += [element]
        encrypted_msg += [row]

    return encrypted_msg


def convert_2D_list(two_d_list):
    """ Receives a 2D list and converts it to a list of strings, each string
    contains the contents of the inner lists. Returns a list of strings"""
    string_lst = []
    for lst in two_d_list:
        string = ''
        for item in lst:
            string += str(item)
            string += ' '
        string += '\n'
        string_lst += [string]
    return string_lst


def check_invertibility(matrix):
    try:
        matrix = np.array(matrix)
        m_inv = np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        return False
    else:
        return True


# call main()
main()

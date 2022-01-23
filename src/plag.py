import numpy as np
# numpy is an open source library for working on multidimensional arrays

import glob
# glob is used to read files of the speciied type

import os

# this is used to interract with the computer's OS

# defining a function to compare the strings using levenshtein's algorithm
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1

    # defining a zero matrix of size of first string * second string
    matrix = np.zeros((size_x, size_y))

    for x in range(size_x):
        matrix[x, 0] = x  # row aray with elements of x
    for y in range(size_y):
        matrix[0, y] = y  # column array with elements of y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:  # if the alphabets at the postion is same
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )

            else:  # if the alphabbets at the position are different
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )

    # returning the levenshtein distance i.e last element of the matrix
    return (matrix[size_x - 1, size_y - 1])


def checkPlagFunc(path):
    plag_percent = int(20)
    # os.chdir(path)
    print(path, 'plag path')
    myFiles = glob.glob(path + '/*.txt')
    print("\nThe text files available are :\n")
    print(myFiles)
    print("\n")
    plag_final = 0
    k = 0
    if (len(myFiles)) < 2:
        return False
    output = {}
    for i in range(0, len(myFiles)):
        for j in range(i, len(myFiles)):

            with open(myFiles[i], 'r') as file:
                data = file.read().replace('\n', '')
                str1 = data.replace(' ', '')
                file1Name = os.path.basename(file.name).replace(".txt", '')

            with open(myFiles[j], 'r') as file:
                data = file.read().replace('\n', '')
                str2 = data.replace(' ', '')
                file2Name = os.path.basename(file.name).replace(".txt", '')

            if (len(str1) > len(str2)):
                length = len(str1)
            else:
                length = len(str2)
            if (myFiles[i] != myFiles[j]):

                plag_final = 100 - round((levenshtein(str1, str2) / length) * 100, 2)
                if (plag_final > plag_percent):
                    print("For the files", file1Name, "and", file2Name, plag_final, "% plagiarised\n")
                    output[file1Name] = {'plag': True, 'plagWith': file2Name, 'plagPercentage': plag_final}
                    output[file2Name] = {'plag': True, 'plagWith': file1Name, 'plagPercentage': plag_final}
                    k = k + 1
                else:
                    print('No Plag', plag_final)

    return output
# performing three types of checking
# one for entire folder with masterfile, one for two separate files , one for all files within the folder

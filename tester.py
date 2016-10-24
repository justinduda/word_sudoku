import sys
import operator


def define_grid():
    grid = []
    empty_spaces = list()
    preset_chars = dict()
    row = 0
    col = 0
    start = True
    with open(sys.argv[1], 'r') as myFile:
        for line in myFile:
            col = 0
            start2 = True
            if start == True:
                start = False
            else:
                row +=1
            new_row = []
            for char in line:
                if start2 == True:
                    start2 = False
                else:
                    col +=1
                if char == '_':
                    empty_spaces.append([row, col])
                    new_row.append('_')
                elif char == '\r' or char == '\n':
                    continue
                else:
                    preset_chars[(row,col)] = char
                    new_row.append(char)
            grid.append(new_row)
    return grid, empty_spaces, preset_chars

def word_list():
    ret_list = []
    with open(sys.argv[2], 'r') as myFile:
        for line in myFile:
            temp_line = []
            for char in line:
                if char == '\r' or char == '\n':
                    pass
                else:
                    temp_line.append(char.upper())
            temp = ''.join(temp_line)
            ret_list.append(temp)
        return ret_list

def main():

    """
        argv[1] == grid file
        argv[2] == word bank file
        argv[3] == steps to solution
        argv[4] == solution file
        """

    myGrid, empty_chars, preset_chars = define_grid()
    myWordList = word_list()
    word_dict = {}
    for elem in myWordList:
        word_dict[elem] = []

        for i in range(0, 8):
            for j in range(0, 8):
                start_coordinates = (i, j)

                # check vertical placement
                vertical_fit = True
                b = j
                for letter in elem:
                    if b <= 8:
                        if myGrid[i][b] == '_' or myGrid == letter:
                            b += 1
                        else:
                            vertical_fit = False    # we know the entire word wont fit for this particular start coordinate
                            break
                # if the word does fit, add the start coordinate to the domain
                if vertical_fit:
                    word_dict[elem].append((start_coordinates, 'V'))

                # check horizontal placement
                horizontal_fit = True
                a = i
                for letter in elem:
                    if a <= 8:
                        if myGrid[a][j] == '_' or myGrid == elem[0]:
                            a += 1
                        else:
                            horizontal_fit = False    # we know the entire word wont fit for this particular start coordinate
                            break
                # if the word does fit, add the start coordinate to the domain
                if horizontal_fit:
                    word_dict[elem].append((start_coordinates, 'H'))

        for elem in word_dict:
            print("WORD: " + elem + ", DOMAIN: " + str(word_dict[elem]) + ", DOMAIN_LENGTH: " + str(len(word_dict[elem])))


        sorted_dict = sorted(word_dict, key=lambda k: len(word_dict[k]))

        for item in sorted_dict:
            print("WORD: " + item + " LENGTH: " + str(len(word_dict[item])))

        # for item in range(0,len(sorted_dict)-1):
        #     print("WORD: " + sorted_dict[item] + ", LENGTH" + str(len(sorted_dict[item])))














    #preset_chars = []

    # # Find all preset characters
    # for x in range(0, 8):
    #     for y in range(0, 8):
    #         if grid[x][y] != '_':
    #             preset_chars.append(grid[x][y], 0)









    # print("BEFORE SORT: " + str(word_dict))
    #
    # for word in word_dict.keys():
    #     for pair in preset_chars:
    #         letter = preset_chars[pair]
    #         if letter in word:
    #             word_dict[word] += 1
    #
    # post_sort = sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)
    #
    # print("AFTER SORT: " + str(post_sort))


if __name__ == '__main__':
    main()

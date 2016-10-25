from sys import argv
import operator
import time
import copy

def define_grid():
    grid = []
    empty_spaces = list()
    preset_chars = dict()
    row = 0
    col = 0
    start = True
    with open(argv[1], 'r') as myFile:
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

class state_node(object):
    def __init__(self, parent=None, options=None, words=None, grid=None, set_char=None, variables=None):
        """parent -> the parent node,
        options -> the different options avalible at this step,
        words-> wordlist,
        grid ->actual grid,
        variables-> the priority to decide where the next word should go"""

        self.parent = parent
        self.options = options
        self.words = words
        self.grid = grid
        self.set_char = set_char
        self.variables = variables


def word_list():
    ret_list = []
    with open(argv[2], 'r') as myFile:
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


def valid_grid(grid):
    """checks if we have a valid grid"""
    #checks rows
    for line in grid:
        rowoccurence = [None, None, None, None, None, None, None, None, None, None]
        for char_index in range(0, len(line)):
            rowoccurence[char_index] = line[char_index]
        if  not len(rowoccurence) != len(set(rowoccurence)):
            return False

    #checks columns
    for i in range(0,9):
        rowoccurence = [None, None, None, None, None, None, None, None, None, None]
        for j in range(0, 9):
            rowoccurence[i] = grid[j][i]
        if not len(rowoccurence) != len(set(rowoccurence)):
            return False

#check 3x3 squares
    check = []
    for j in range(3, 12, 3):
        check = []
        for i in range (0,3):
            check.extend(grid[i][:j])
        if not len(check) != len(set(check)):
            return False
        check = []
        for i in range(3, 6):
            check.extend(grid[i][:j])
        if not len(check) != len(set(check)):
            return False
        check = []
        for i in range(6, 9):
            check.extend(grid[i][:j])
        if not len(check) != len(set(check)):
            return False

    return True

def complete_grid(grid):
    """check if the grid is completely filled not IF IT IS SOLVED!!!"""
    for line in grid:
        if '_' in line:
            return False
    return True

def backtracking_search(state):
    return recursive_backtracking(state)

def print_clean_grid(Grid):
    for list in Grid:
        my_string = []
        for char in list:
            if char == None:
                my_string.append('_')
            else:
                my_string.append(char)
        my_string.append('\n')
        print(''.join(my_string))

def delete_word(val, dir, space_tuple, grid):
    """deletes the word from the grid"""
    if dir == 'h':
        for y in range(space_tuple[1], space_tuple[1] + len(val)):
            grid[space_tuple[0]][y] = '_'
    if dir == 'v':
        for x in range(space_tuple[0], space_tuple[0] + len(val)):
            grid[x][space_tuple[1]] = '_'
    return grid


def print_starting_point(grid,coor):
    row = 0
    for list in grid:
        col = 0
        my_string = []
        for char in list:
            if coor == (row,col):
                my_string.append('*')
            else:
                if char == None:
                    my_string.append('_')
                else:
                    my_string.append(char)
            col += 1
        row += 1
        my_string.append('\n')
        print(''.join(my_string))


def check_can_fit(dir, val, start):
    """Checks if the word can even fit in the space given"""
    if dir == 'v':
        if start[1]+ len(val) > 9:
            print 'nope'
            return False
        return True
    else:
        if start[0] +len(val) > 9:
            return False
        return True


def check_horizontal(state, space_tuple, word):
    count = 0
    try:
        for y in range( space_tuple[1], space_tuple[1] + len(word)):
            #if we find a letter that shouldnt be there
            if state.grid[space_tuple[0]][y] == '_' or state.grid[space_tuple[0]][y] == word[y - space_tuple[1]]:
                count+=1
    except IndexError:
        return False

    if count == len(word):
        return True
    return False

def check_vertical(state, space_tuple, word):
    count = 0
    try:
        for x in range(space_tuple[0], space_tuple[0] + len(word)):
            if state.grid[x][space_tuple[1]] == '_' or state.grid[x][space_tuple[1]] == word[x - space_tuple[0]]:
                count+=1
    except IndexError:
        return False
    if count == len(word):
        return True
    return False

def check_valid_fit(state, space_tuple, word, dir):
    temp_grid = state.grid
    edited_temp_grid = put_word_in_temp_grid(temp_grid, space_tuple, word, dir)
    if valid_grid(edited_temp_grid):
        state.grid = edited_temp_grid
        return True
    return False


def put_word_in_temp_grid(temp_grid, space_tuple, word, dir):
    if dir == 'v':
        for x in range(space_tuple[0], space_tuple[0] + len(word)):
            temp_grid[x][space_tuple[1]] = word[x - space_tuple[0]]
        return temp_grid
    if dir == 'h':
        for y in range(space_tuple[1], space_tuple[1] + len(word)):
            temp_grid[space_tuple[0]][y] = word[y - space_tuple[1]]
        return temp_grid

def nikku_algo():
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
                            vertical_fit = False  # we know the entire word wont fit for this particular start coordinate
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
                            horizontal_fit = False  # we know the entire word wont fit for this particular start coordinate
                            break
                # if the word does fit, add the start coordinate to the domain
                if horizontal_fit:
                    word_dict[elem].append((start_coordinates, 'H'))
    return word_dict


def next_state(state):
    stateList = []
    word_dict = nikku_algo()
    #word = state.options.pop(0)
    for word in state.options:
        for space_tuple in word_dict[word]:
            #set some variables
            temp_grid = copy.deepcopy(state.grid)
            state_new = state_node(None, state.options, state.words, temp_grid, state.set_char, state.variables)
            dir = space_tuple[1]
            space = space_tuple[0]
            #Lets try vertical now
            if dir == 'V':
                if check_vertical(state_new, space, word):
                    if check_valid_fit(state_new, space, word, 'v'):
                        stateList.append(state_new)
                        #print 'V'
                        #time.sleep(2)
            #Lets try horizontal now
            else:
                if check_horizontal(state_new, space, word):
                    if check_valid_fit(state_new, space, word, 'h'):
                        stateList.append(state_new)
                        #print 'H'
                        #print_clean_grid(temp_grid)
                        #time.sleep(2)
        state.options.remove(word)

    return stateList





def recursive_backtracking(state):
    nextStates = next_state(state)
    if len(nextStates):
        if complete_grid(state.grid):
            print_clean_grid(state.grid)
            return state
        else:
            print 'failing'
            return None
    for state in nextStates:
        ret =  recursive_backtracking(state)
        if ret:
            return ret
    print 'failing'
    return None

# def recursive_backtracking(state):
#     if state.parent == None:
#         state_new = state_node(state, state.options, state.words, state.grid, state.set_char, state.variables)
#     # if complete_grid(state.grid):
#     #     return
#     else:
#         state_new = state
#
#
#     space_tuple = state.variables[0][0]
#     word = state.options[0]
#     print word
#     print space_tuple
#     print_clean_grid(state.grid)
#     print ''
#     print_starting_point(state.grid, space_tuple)
#     print ''
#
#     word_put_in = False
#     if check_horizontal(state, space_tuple, word):
#         if check_valid_fit(state, space_tuple, word, 'h'):
#             word_put_in = True
#             #we need to make a new node parent is the current node
#             options =  state.options
#             options.remove(word)
#             variables = state.variables
#             variables.pop(0)
#             state = state_node(state, options, state.words, state.grid, state.set_char, variables)
#             recursive_backtracking(state)
#             #ret_val = recursive_backtracking(state)
#             #if ret_val != "Fail":
#             #    return state.grid
#
#     if check_vertical(state, space_tuple, word) and not word_put_in:
#         if check_valid_fit(state, space_tuple, word, 'v'):
#             #we need to make a new node parent is the current node
#             options = state.options
#             options.remove(word)
#             variables = state.variables
#             variables.pop(0)
#             state = state_node(state, options, state.words, state.grid, state.set_char, variables)
#             recursive_backtracking(state)
#             #ret_val = recursive_backtracking(state)
#             #if ret_val != 'Fail':
#             #    return state.grid
#             # else:
#             #     options = state.options
#             #     options.remove(word)
#             #     variables = state.variables
#             #     variables.pop(0)
#             #     state = state_node(state, options, state.words, state.grid, state.set_char, variables)
#
#    # if complete_grid(state):
#    #     return state.grid
#    # else:
#    #     return 'Fail'
#
#     #go back up the tree!!!
#     if len(state.options) == 1:
#         ret_val = 'Fail'
#         return ret_val
#
#     #the word didn't work so we need to try and different word under our parent
#     options = state.options
#     options.remove(word)
#     variables = state.variables
#     variables.pop(0)
#     state = state_node(state.parent, options, state.words, state.grid, state.set_char, variables)
#     recursive_backtracking(state)
#
#     #return
#


def square_constraints(grid, i, j):
    start_x = i+3 % 3
    start_y = j+3 % 3

    constraints = 0
    for x in range(start_x, start_x+2):
        for y in range(start_y, start_y+2):
            if grid[x][y] != '_':
                constraints += 1
    return constraints

def x_constraints(grid, i, j):
    constraints = 0
    for x in range(0, 8):
        if grid[x][j] != '_':
            constraints += 1
    return constraints

def y_constraints(grid, i, j):
    constraints = 0
    for y in range(0, 8):
        if grid[i][y] != '_':
            constraints += 1
    return constraints

def constraints(grid, i, j):
    return square_constraints(grid, i, j) + x_constraints(grid, i, j) + y_constraints(grid, i, j)



#     new_options = state.options
#     new_options = new_options.remove(value)
#     new_grid =
#     new_spaces = sorted(state.variables.items(), key=operator.itemgetter(1))
#     newState = state_node(state, new_options, state.myWordList, state.myGrid, state.preset_chars, new_spaces)
#     recursive_backtracking(newState)
# else:
#     #we need to remove the word cause it doesnt fit
#     state.grid = delete_word(value, 'h', space_tuple, state.grid)
#     #maybe worry about the root case?
#     if len(state.options) == 0:
#         pass
#         #we need to go back up
#     else:
#
#     state.options.remove(value)
#     new_spaces = sorted(state.variables.items(), key=operator.itemgetter(1))
#     newState = state_node(state, state.options, state.myWordList, state.myGrid, state.preset_chars, new_spaces)
#     recursive_backtracking(newState)
#     #not at root so make a new node from this states parent
#     else:
#
#
#         state.parent.options.remove(value)
#         new_spaces = sorted(state.variables.items(), key=operator.itemgetter(1))
#

# newState = state_node(state.parent, state.parent.options, myWordList, myGrid, preset_chars, new_spaces)






"""
    argv[1] == grid file
    argv[2] == word bank file
    argv[3] == steps to solution
    argv[4] == solution file
    """
def main():
    # make a grid object which contains space objects
    myGrid, empty_chars, preset_chars = define_grid()
    myWordList = word_list()
    #myWordList.sort(lambda  x,y: cmp(len(x), len(y)))
    myWordList= sorted(myWordList, key=lambda x: len(x))

    # create priority structure
    unprioritized_variables = {}
    for i in range(0, 8):
        for j in range(0, 8):
            unprioritized_variables[(i, j)] = constraints(myGrid, i, j)
    variables = sorted(unprioritized_variables.items(), key=operator.itemgetter(1), reverse=True)

    if preset_chars != None:
        rootState = state_node(None, myWordList, myWordList, myGrid, preset_chars, variables)
    else:
        rootState = state_node(None, myWordList, myWordList, myGrid, preset_chars, variables)


    #print_clean_grid(myGrid)

    state = backtracking_search(rootState)
    print_clean_grid(state.grid)







if __name__ == '__main__':
    main()

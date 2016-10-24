from sys import argv
import operator

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


def valid_grid(state):
    """checks if we have a valid grid"""
    #checks rows
    for line in state.grid:
        rowoccurence = [None, None, None, None, None, None, None, None, None, None]
        for char_index in range(0, len(line)):
            rowoccurence[char_index] = line[char_index]
        if  not len(rowoccurence) != len(set(rowoccurence)):
            return False

    #checks columns
    for i in range(0,9):
        rowoccurence = [None, None, None, None, None, None, None, None, None, None]
        for j in range(0, 9):
            rowoccurence[i] = state.grid[j][i]
        if not len(rowoccurence) != len(set(rowoccurence)):
            return False

#check 3x3 squares
    check = []
    for j in range(3, 12, 3):
        check = []
        for i in range (0,3):
            check.extend(state.grid[i][:j])
        if not len(check) != len(set(check)):
            return False
        check = []
        for i in range(3, 6):
            check.extend(state.grid[i][:j])
        if not len(check) != len(set(check)):
            return False
        check = []
        for i in range(6, 9):
            check.extend(state.grid[i][:j])
        if not len(check) != len(set(check)):
            return False

    return True

def complete_grid(state):
    """check if the grid is completely filled not IF IT IS SOLVED!!!"""
    for line in state.grid:
        if None in line:
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


def recursive_backtracking(state):
    # if not valid_grid(state):
    #     state = state.parent
    # #return invalidstate() --> I think you need to go back up the tree here
    # if complete_grid(state):
    #     return state

# Find most constrained variables
# Assign least constraining value to it (try vertically and then horizontally)
# Check if assignment is legal
# if assignment is legal then recurse on next most constrained variable
# if assignment is illegal then backtrack to last legal instance of the grid
# Try assigning the next least constraining value to the current variable
# recurse

    print state.variables[0][0]

    space_tuple = state.variables[0][0]
    value = state.options[0]
    #check if the space_tuple is a letter, if so lets use that
    if (space_tuple[0], space_tuple[1]) in state.set_char.keys():
        letter = state.set_char[(space_tuple[0],space_tuple[1])]
        for elem in state.options:
            if elem[0] == letter:
                value = elem
                break


    print value

    word_done = False
    print_starting_point(state.grid, space_tuple)
    print ''

    # horz attempt
    horz_succeeded = True
    #check if the word will even fit
    if check_can_fit('h',value,space_tuple):
        for y in range(space_tuple[1], space_tuple[1] + len(value)):
            #current grid index = _ OR index is already = to that letter
            if state.grid[space_tuple[0]][y] == '_' or state.grid[space_tuple[0]][y] == value[y - space_tuple[1]]:
                #set the index to the char
                state.grid[space_tuple[0]][y] = value[y - space_tuple[1]]
                #####need to add the letter to the preset_chars
                #####state.set_char[space_tuple[0][y]] = value[y - space_tuple[1]]   ##-----> when we remove the letters we need to remove from this
                #check some length??
                if y - space_tuple[1] == len(value): #----> len(value) -1
                    word_done = True
            #if the index isn't that letter or _
            else:
                if (space_tuple[0], y) in state.set_char.keys():
                    break
                #if it is a letter
                while state.grid[space_tuple[0]][space_tuple[1]] != '_':
                    #if it isnt one of the preset chars
                    if not (space_tuple[0],y) in state.set_char.keys():
                        #set it back to a blank
                        state.grid[space_tuple[0]][y] = '_'
                    #go back one
                    y -= 1
                    #it fails in putting a word
                    horz_succeeded = False
                break
        print_clean_grid(state.grid)
        print ''
    else:
        horz_succeeded = False
    if horz_succeeded:
        if valid_grid(state):
        #Remove variable and value from respective queues
            # if not word_done:
            #     state.parent.options.remove(value)
            #     variables = sorted(state.variables.items(), key=operator.itemgetter(1))
            #     state.variables = variables
            #     if state.parent != None:
            #         recursive_backtracking(state.parent)
            # else:
            #     variables = sorted(state.variables.items(), key=operator.itemgetter(1))
            #     rootState = state_node(None, myWordList, myWordList, myGrid, preset_chars, variables)
            if word_done:
                new_options = state.options
                new_options.remove(value)
                new_spaces = state.variables
                new_spaces.pop(0)
                newState = state_node(state, new_options, state.words, state.grid, state.set_char, new_spaces)
                print_clean_grid(state.grid)
                print ''
                recursive_backtracking(newState)
            else:
                new_options = state.options
                new_options.remove(value)
                new_spaces = state.variables
                new_spaces.pop(0)
                newState = state_node(state, new_options, state.words, state.grid, state.set_char, new_spaces)
                print_clean_grid(state.grid)
                print ''
                recursive_backtracking(newState)

        else:
            return



    # vert attempt
    vert_succeeded = True
    if check_can_fit('v', value, space_tuple):
        for x in range(space_tuple[0], space_tuple[0] + len(value)):
            if state.grid[x][space_tuple[1]] == '_' or state.grid[x][space_tuple[1]] == value[x - space_tuple[0]]:
                state.grid[x][space_tuple[1]] = value[x - space_tuple[0]]
                if x - space_tuple[1] == len(value): #----> len(value) -1
                    word_done = True
            else:
                while state.grid[space_tuple[0]][space_tuple[1]] != '_':
                    if not (space_tuple[0], space_tuple[1]) in state.set_char.keys():
                        state.grid[x][space_tuple[1]] = '_'
                    x -= 1
                    vert_succeeded = False
                break
    else:
        print 'whyyy'
        vert_succeeded = False
    if vert_succeeded:
        print 'in here'
        if valid_grid(state):
            # Remove variable and value from respective queues
            #if not word_done:
            #    state.options.remove(value)
            #    variables = sorted(state.variables.items(), key=operator.itemgetter(1))
            #    state.variables = variables
            #    recursive_backtracking(state)
            #below would be under the an else for the above if
            if word_done:
                new_options = state.options
                new_options.remove(value)
                new_spaces = state.variables
                new_spaces.pop(0)
                print_clean_grid(state.grid)
                print ''
                newState = state_node(state, new_options, state.words, state.grid, state.set_char, new_spaces)
                recursive_backtracking(newState)

        else:
            print 'we need to delete the word make a new node--> under the same parent and minus word from state.options'
    else:
        state.options.remove(value)
        print_clean_grid(state.grid)
        print ''
        newState = state_node(state, state.options, state.words, state.grid, state.set_char, state.variables)
        recursive_backtracking(state)
    return

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
    print myWordList
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


    #"parent -> the parent node, options -> the different options avalible at this step,    words-> wordlist  grid ->actual grid variables-> the words left in the word bank"""
    #print_clean_grid(myGrid)

    backtracking_search(rootState)


#make a node object for each different game option
#the node should list the different possibilities so it is easy to back trace
#define the most constrained variables
#most stuff in the column, row, in the cell --> we can figure this out by looking at the space objects
#but would it be easier to check column, row, cell indivually? and we wouldnt need the space object just put a value
#define the least constraining vairables
# most stuff in the column, row, in the cell --> we can figure this out by looking at the space objects
# but would it be easier to check column, row, cell indivually? and we wouldnt need the space object just put a value
#define the most constraining variables
#smallest word in the word bank

#depth-first search
#call backtracking algo

#how to incorporate the wrong words in the word bank????





if __name__ == '__main__':
    main()

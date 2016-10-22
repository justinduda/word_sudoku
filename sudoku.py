from sys import argv

def define_grid():
    grid = []
    empty_spaces = list()
    preset_chars = dict()
    row = 0
    col = 0
    start = True
    with open(argv[1], 'r') as myFile:
        for line in myFile:
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
    def __init__(self, parent=None, options=None, words=None, grid=None, set_char=None):
        """parent -> the parent node, options -> the different options avalible at this step, words-> wordlist,  grid ->actual grid variables-> the words left in the word bank"""
        self.parent = parent
        self.options = options
        self.words = words
        self.grid = grid
        self.set_char = set_char


def word_list():
    ret_list = []
    with open(argv[2], 'r') as myFile:
        for line in myFile:
            temp_line = []
            for char in line:
                if char == '\r' or char == '\n':
                    pass
                else:
                    temp_line.append(char)
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
        print ''.join(my_string)

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

    variable = (0, 0)
    #print state.words
    value = state.options[0]
    word_done = False

    # vertical attempt
    vertical_succeeded = True
    for y in range(variable[1], variable[1] + len(value)):
        #current grid element = _ or
        if state.grid[variable[0]][y] == '_' or state.grid[variable[0]][y] == value[y - variable[1]]:
            #print 'in herey'
            #print "grid letter: " + state.grid[y][variable[1]] + " word letter: " + value[y - variable[0]]
            state.grid[variable[0]][y] = value[y - variable[1]]
            #print_clean_grid(state.grid)
            #print 'if'
            if y - variable[1] == len(value) - 1:
                word_done = True
        else:
            while state.grid[variable[0]][variable[1]] != '_':
                if not (variable[0],y) in state.set_char.keys():
                    state.grid[variable[0]][y] = '_'
                    #print_clean_grid(state.grid)
                    #print 'else'
                y -= 1
                vertical_succeeded = False
            break
    if vertical_succeeded:
        if valid_grid(state):
            # Remove variable and value from respective queues
            if not word_done:
                state.options.remove(value)
                recursive_backtracking(state)
            print_clean_grid(state.grid)
        else:
            return

    # horizontal attempt
    horizontal_succeeded = True
    for x in range(variable[0], variable[0] + len(value)):
        if state.grid[x][variable[1]] == '_' or state.grid[x][variable[1]] == value[x - variable[0]]:
            #print 'in here2'
            #print "grid letter: " + state.grid[x][variable[1]] + " word letter: " + value[x - variable[0]]
            state.grid[x][variable[1]] = value[x - variable[0]]
            if x - variable[1] == len(value) - 1:
                word_done = True
        else:
            #print 'in here'
            while state.grid[variable[0]][variable[1]] != '_':
                if not (variable[0], variable[1]) in state.set_char.keys():
                    #print("letter deleted: " + state.grid[variable[0], variable[1]])
                    state.grid[x][variable[1]] = '_'
                x -= 1
                horizontal_succeeded = False
            break
    if horizontal_succeeded:
        if valid_grid(state):
            # Remove variable and value from respective queues

            if not word_done:
                state.options.remove(value)
                recursive_backtracking(state)
            print_clean_grid(state.grid)
    return

#make a priority queue ---> most contraint variables if tie then most constraining variable
#for x in priority_queue
#make a priority queue2 ---> values that are least constraining
#   for y in priority_queue2
#       set the x y in the grid
#   new_node = backtrack(cur_node)
#   if new_node is invalid()
#       unset new_node
#   else:
#       return new_node

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
    if preset_chars != None:
        rootState = state_node(None, myWordList, myWordList, myGrid, preset_chars)
    else:
        rootState = state_node(None, myWordList, myWordList, myGrid, preset_chars)
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

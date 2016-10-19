from sys import argv

class Grid:
    def __init__(self):
        self.grid = []
        self.empty_spaces = list()
        self.preset_chars = list()
        row = 0
        col = 0
        with open(argv[1], 'r') as myFile:
            for line in myFile:
                row +=1
                new_row = []
                for char in line:
                    col +=1
                    if char == '_':
                        self.empty_spaces.append([row, col])
                        new_row.append(None)
                    elif char == '\r' or char == '\n':
                        continue
                    else:
                        self.preset_chars.append(char)
                        new_row.append(char)
                self.grid.append(new_row)

class state_node(object):
    def __init__(self, parent=None, options=None, words=None, grid = None, empty_spaces=None):
        """parent -> the parent node, options -> the different options avalible at this step, variables-> the words left in the word bank"""
        self.parent = parent
        self.options = options
        self.words = words
        self.cur_grid = grid


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
            ret_list.append(''.join(temp_line))
    return ret_list

def backtracking_search(state):
    return recursive_backtracking(state)

def valid_grid(state):
    """checks if we have a valid grid"""
    #checks rows
    for line in state.cur_grid:
        rowoccurence = [None, None, None, None, None, None, None, None, None, None]
        for char_index in range(0, len(line)):
            rowoccurence[char_index] = line[char_index]
        if  not len(rowoccurence) != len(set(rowoccurence)):
            return False

    #checks columns
    for i in range(0,9):
        rowoccurence = [None, None, None, None, None, None, None, None, None, None]
        for j in range(0, 9):
            rowoccurence[i] = state.cur_grid[j][i]
        if not len(rowoccurence) != len(set(rowoccurence)):
            return False

    #check 3x3 squares
    check = []
    for j in range(3, 12, 3):
        check = []
        for i in range (0,3):
            check.extend(state.cur_grid[i][:j])
        if not len(check) != len(set(check)):
            return False
        check = []
        for i in range(3, 6):
            check.extend(state.cur_grid[i][:j])
        if not len(check) != len(set(check)):
            return False
        check = []
        for i in range(6, 9):
            check.extend(state.cur_grid[i][:j])
        if not len(check) != len(set(check)):
            return False

    return True

def complete_grid(state):
    """check if the grid is completely filled not IF IT IS SOLVED!!!"""
    for line in state.cur_grid:
        if None in line:
            return False
    return True

def recursive_backtracking(state):
    if not valid_grid(state):
        state = state.parent
        #return invalidstate() --> I think you need to go back up the tree here
    if complete_grid(state):
       return state

    n = 0

    while not complete_grid(state):
            curr_word = state.words[n]
            if state.cur_grid[i][j] == None:
                vert_iterator = j
                while vert_iterator != 9:
                    if state.cur_grid[i][vert_iterator] == None:
                        state.cur_grid[i][vert_iterator] = curr_word[0]
                        curr_word = curr_word[1:]
                    else:
                        if state.cur_grid[i][vert_iterator] == curr_word[0]:
                            state.cur_grid[i][vert_iterator] = curr_word[0]
                            curr_word = curr_word[1:]
                        else:
                            while vert_iterator != j:
                                state.cur_grid[i][vert_iterator] = None
                                break
                            break
            n += 1




    state.words


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
    myGrid = Grid()
    myWordList = word_list()
    myWordList.sort(lambda  x,y: cmp(len(x), len(y)))
    print myWordList
    if myGrid.preset_chars != None:
        rootState = state_node(myGrid.preset_chars, myWordList, None, myGrid, myGrid.empty_spaces)
    else:
        rootState = state_node(None, myWordList, None, myGrid, myGrid.empty_spaces)
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

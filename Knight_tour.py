#created classe to prevent possible errors, This function is called later 
class PathFound(RuntimeError):
    pass


#here we are creating game board  
class KNIGHTSgame:
    # i am initialising the program
    
    def __init__(self, size, structure):
        
        #i am creating the game, starting my inialising process
        self.width = size[0]
        self.height = size[1]
        self.initial_position = (0, 0)

        self.structure = structure
        self.reserved_positions = []

        self.closed_tour = False
        self.closed_positions = []

        self.board = []
        self.create_board()

    def create_board(self):
 
        # creating the first loop to 
        for i in range(self.height):
            self.board.append([0]*self.width)

        for l in structure.keys():
            self.reserved_positions.append(structure[l])


    def print_board(self):
        # creating my board , building an X and Y grid chart
        print ("  ")
        print ("------")
        for line in self.board:
            print (line)
           
        print ("------")
        print ("  ")



    def create_possible_moves(self, curr_pos):
        
       #defining what are the possible moves that my knoght can make 
        probable_pos  = []
        move_places = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                        (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for move in move_places:
            XNew = curr_pos[0] + move[0]
            YNew = curr_pos[1] + move[1]

            if (XNew >= self.height):
                continue
            elif (XNew < 0):
                continue
            elif (YNew >= self.width):
                continue
            elif (YNew < 0):
                continue
            else:
                probable_pos.append((XNew, YNew))

        return probable_pos


    def sort_lone_neighbors(self, visit_spot):
        """
        Checking to see what spaces are avaible and the lonely spaces based which neighbors are avaible to meet with 
        """
        neighbor_list = self.create_possible_moves(visit_spot)
        empty_neighbours = []

        for neighbor in neighbor_list:
            no_value = self.board[neighbor[0]][neighbor[1]]
            if (no_value == 0) and (neighbor not in self.reserved_positions):
                empty_neighbours.append(neighbor)

        scores = []
        for empty in empty_neighbours:
            score = [empty, 0]
            moves = self.create_possible_moves(empty)
            for m in moves:
                if self.board[m[0]][m[1]] == 0:
                    score[1] += 1
            scores.append(score)

        scores_sort = sorted(scores, key = lambda s: s[1])
        sorted_neighbours = [s[0] for s in scores_sort]
        return sorted_neighbours

    def tour(self, n, path, visit_spot):
        """
        defining the recurive facotors that I took 
        """
        self.board[visit_spot[0]][visit_spot[1]] = n
        path.append(visit_spot) #
        print ("Visiting: ", visit_spot)

        if n == self.width * self.height: #if every grid is filled
            if self.closed_tour:
                if path[-1] in self.closed_positions:
                    self.path = path
                    raise PathFound
                else:
                    print("Not a tour")
                    self.board[visit_spot[0]][visit_spot[1]] = 0
                    try:
                        path.pop()
                    except IndexError:
                        raise Exception("No successful path was found")
            else:
                self.path = path
                raise PathFound
        else:
            rule_location = self.structure.get(n+1, None)
            if rule_location is None:
                sorted_neighbours = self.sort_lone_neighbors(visit_spot)
                for neighbor in sorted_neighbours:
                    self.tour(n+1, path, neighbor)
            else:
                if rule_location in self.create_possible_moves(visit_spot):
                    print("Obeying rule: ", rule_location)
                    self.tour(n+1, path, rule_location)

            #If we exit this loop, all neighbours failed so we reset
            self.board[visit_spot[0]][visit_spot[1]] = 0
            try:
                path.pop()
                print( "Going back to: ", path[-1])
            except IndexError:
                raise Exception("No successful path was found")

#i am looking a path ion how to miovce from one quarident to another 
    def look_for_path(self, n, path, start):
        try:
            if self.closed_tour:
                self.closed_positions = self.create_possible_moves(self.initial_position)
            self.tour(n, path, start)
        except PathFound:
        

            return self.path

if __name__ == '__main__':
    # structure = {2:(2,1), 3:(3,3)} #example possible structureet
    # structure = {2:(2,1), 3:(4,4)} #example impossible structureet
    structure = {}

    #Define the size of the board
    kg = KNIGHTSgame(size=(10, 10), structure=structure)
    
    kg.initial_position = (0,0)

    kg.look_for_path(1, [], kg.initial_position)
    kg.print_board()
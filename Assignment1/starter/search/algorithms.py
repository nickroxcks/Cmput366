import heapq

class State:
    """
    Class to represent a state on grid-based pathfinding problems. The class contains two static variables:
    map_width and map_height containing the width and height of the map. Although these variables are properties
    of the map and not of the state, they are used to compute the hash value of the state, which is used
    in the CLOSED list. 

    Each state has the values of x, y, g, h, and cost. The cost is used as the criterion for sorting the nodes
    in the OPEN list for both Dijkstra's algorithm and A*. For Dijkstra the cost should be the g-value, while
    for A* the cost should be the f-value of the node. 
    """
    map_width = 0
    map_height = 0
    
    def __init__(self, x, y):
        """
        Constructor - requires the values of x and y of the state. All the other variables are
        initialized with the value of 0.
        """
        self._x = x
        self._y = y
        self._g = 0
        self._h = 0
        self._cost = 0
        
    def __repr__(self):
        """
        This method is invoked when we call a print instruction with a state. It will print [x, y],
        where x and y are the coordinates of the state on the map. 
        """
        state_str = "[" + str(self._x) + ", " + str(self._y) + "]"
        return state_str
    
    def __lt__(self, other):
        """
        Less-than operator; used to sort the nodes in the OPEN list
        """
        return self._cost < other._cost
    
    def state_hash(self):
        """
        Given a state (x, y), this method returns the value of x * map_width + y. This is a perfect 
        hash function for the problem (i.e., no two states will have the same hash value). This function
        is used to implement the CLOSED list of the algorithms. 
        """
        return self._y * State.map_width + self._x
    
    def __eq__(self, other):
        """
        Method that is invoked if we use the operator == for states. It returns True if self and other
        represent the same state; it returns False otherwise. 
        """
        return self._x == other._x and self._y == other._y

    def get_x(self):
        """
        Returns the x coordinate of the state
        """
        return self._x
    
    def get_y(self):
        """
        Returns the y coordinate of the state
        """
        return self._y
    
    def get_g(self):
        """
        Returns the g-value of the state
        """
        return self._g
        
    def get_h(self):
        """
        Returns the h-value of the state
        """
        return self._h
    
    def get_cost(self):
        """
        Returns the cost of the state (g for Dijkstra's and f for A*)
        """
        return self._cost
    
    def set_g(self, cost):
        """
        Sets the g-value of the state
        """
        self._g = cost
    
    def set_h(self, h):
        """
        Sets the h-value of the state
        """
        self._h = h
    
    def set_cost(self, cost):
        """
        Sets the cost of a state (g for Dijkstra's and f for A*)
        """
        self._cost = cost

class Search:
    """
    Interface for a search algorithm. It contains an OPEN list and a CLOSED list.

    The OPEN list is implemented with a heap, which can be done with the library heapq
    (https://docs.python.org/3/library/heapq.html).    
    
    The CLOSED list is implemented as a dictionary where the state hash value is used as key.
    """
    def __init__(self, gridded_map):
        self.map = gridded_map
        self.OPEN = []
        self.CLOSED = {}
    
    def search(self, start, goal):
        """
        Search method that needs to be implemented (either Dijkstra or A*).
        """
        raise NotImplementedError()
            
class Dijkstra(Search):
            
    def search(self, start, goal):
        """
        Disjkstra's Algorithm: receives a start state and a goal state as input. It returns the
        cost of a path between start and goal and the number of nodes expanded.

        If a solution isn't found, it returns -1 for the cost.
        """

        """
        OPEN is heapq where each item is a STATE
        CLOSED is a dictionary where keys are the hashvalue of the STATE. The STATE is the value of the dict entry
        """
        # insert start to open and close list. Use the closes state in memory to auto update state in open list
        self.CLOSED[start.state_hash()] = start
        heapq.heappush(self.OPEN, self.CLOSED[start.state_hash()])

        num_nodes_expanded = 0  # since we are required to return the number of nodes expanded, use this

        while self.OPEN:  # loop while the open list is not empty
            n = heapq.heappop(self.OPEN)  # get the cheapest value. heapq should take care of this
            num_nodes_expanded += 1
            if n.state_hash() == goal.state_hash():
                self.OPEN = []  # clean lists because it looks like test cases use the same Search instance each time
                self.CLOSED = {}
                return n.get_g(), num_nodes_expanded
            for n_prime in self.map.successors(n):  # n_prime is a neighbor of n. For all neighbors in n...
                n_prime.set_cost(n_prime.get_g())  # doesn't look like successor function sets cost. so manually do it
                if n_prime.state_hash() not in self.CLOSED:  # if this neighbor is a new node
                    n_prime.set_cost(n_prime.get_g())  # cost should be g(n) + C(n,n_prime). this is the g value of n'
                    self.CLOSED[n_prime.state_hash()] = n_prime  # add to open and closed list
                    heapq.heappush(self.OPEN, self.CLOSED[n_prime.state_hash()])
                # n_prime already expanded, but a cheaper path was found
                if n_prime.state_hash() in self.CLOSED and n_prime.get_g() < self.CLOSED[n_prime.state_hash()].get_g():
                    self.CLOSED[n_prime.state_hash()].set_g(n_prime.get_g())  # implicitly this updates open as well
                    self.CLOSED[n_prime.state_hash()].set_cost(n_prime.get_g())
                    heapq.heapify(self.OPEN)  # ensures we can get cheapest value next time
        self.OPEN = []
        self.CLOSED = {}  # clean lists because it looks like test cases use the same Search instance each time
        return -1, 0  # if we cant find solution, return this

''' 
note:  since we are given a consistent heuristic, this function is not general, and assumes consistent heuristic
note2: since A* is the exact same as Dijkstra except using f values,
       and we are guaranteed a consistent heuristic, use same code but with f values as cost instead
'''
class AStar(Search):

    # given a state, find the hvalue. function returns the h value
    def h_value(self, state, goal):

        delta_x = abs(goal.get_x() - state.get_x())
        delta_y = abs(goal.get_y() - state.get_y())
        h_s = max(delta_x, delta_y) + 0.5*min(delta_x, delta_y)

        # return h_s
        return 2 * h_s


            
    def search(self, start, goal):
        """
        A* Algorithm: receives a start state and a goal state as input. It returns the
        cost of a path between start and goal and the number of nodes expanded.

        If a solution isn't found, it returns -1 for the cost.
        """
        # insert start to open and close list. Use the closes state in memory to auto update state in open list
        self.CLOSED[start.state_hash()] = start
        heapq.heappush(self.OPEN, self.CLOSED[start.state_hash()])

        num_nodes_expanded = 0  # since we are required to return the number of nodes expanded, use this

        while self.OPEN:  # loop while the open list is not empty
            n = heapq.heappop(self.OPEN)  # get the cheapest value. heapq should take care of this
            num_nodes_expanded += 1
            if n.state_hash() == goal.state_hash():
                self.OPEN = []  # clean lists because it looks like test cases use the same Search instance each time
                self.CLOSED = {}
                return n.get_g() + self.h_value(n, goal), num_nodes_expanded
            for n_prime in self.map.successors(n):  # n_prime is a neighbor of n. For all neighbors in n...
                n_prime.set_cost(n_prime.get_g() + self.h_value(n_prime, goal))  # doesn't look like successor function sets cost. so manually do it
                if n_prime.state_hash() not in self.CLOSED:  # if this neighbor is a new node
                    n_prime.set_cost(n_prime.get_g() + self.h_value(n_prime, goal))  # cost should be g(n) + C(n,n_prime). this is the g value of n'
                    self.CLOSED[n_prime.state_hash()] = n_prime  # add to open and closed list
                    heapq.heappush(self.OPEN, self.CLOSED[n_prime.state_hash()])
                # n_prime already expanded, but a cheaper path was found
                if n_prime.state_hash() in self.CLOSED and n_prime.get_g() + self.h_value(n_prime, goal)\
                        < self.CLOSED[n_prime.state_hash()].get_g() + self.h_value(self.CLOSED[n_prime.state_hash()], goal):
                    self.CLOSED[n_prime.state_hash()].set_g(n_prime.get_g())  # implicitly this updates open as well
                    self.CLOSED[n_prime.state_hash()].set_cost(n_prime.get_g() + self.h_value(n_prime, goal))
                    heapq.heapify(self.OPEN)  # ensures we can get cheapest value next time
        self.OPEN = []
        self.CLOSED = {}  # clean lists because it looks like test cases use the same Search instance each time
        return -1, 0  # if we cant find solution, return this
# Import the GUI Module.
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Import Matrix generator module
import numpy

FRAME_WIDTH = 500
DEFAULT_SIZE = 50
DEFAULT_PROBABILITY = 0.2
PATH_NOT_FOUND = "Path not found"
PATH_FOUND = "Found path"


class Map:
    def __init__(self, size, probability):
        """Initialize a new map object.
        Args:
            size (int): size of map 10 - 1000
            probability (double): 0.0 - 1.0 (0: all empty cells, 1: all walls)
        Returns:
            map object (n*n matrix) with n*n*p empty cells and n*n*(1-p) filled cells
        """
        self.size = size
        self.probability = probability

        # Check if arguments are valid
        if probability > 1 or probability < 0:
            raise ValueError("probability is in range 0 and 1")

        # Generate a uniform distribution matrix (values range from 0.0 to 1.0)
        self.map = numpy.random.uniform(size=[size, size])
        # Generate matrix with n*n*p empty cells
        self.map = (self.map < probability).astype(int)

        # Set start and finish
        self.map[0, 0] = self.map[size - 1, size - 1] = 0

        # Path from start to finish
        self.solved_path = ["N/A", "N/A", []]

    def connected_cells(self, cell):
        """
        Find all connected cells around a cell
        :param cell: list of (x, y) coordinate of a cell in a numpy array
        :return:
        """
        x = cell[0]
        y = cell[1]
        connected_cells = set()
        all_possible_cells = [(x, y-1), (x+1, y), (x, y+1), (x-1,y)]
        for (i, j) in all_possible_cells:
            if self.in_bounds((i, j)):
                if self.map[i, j] == 0:
                    connected_cells.add((i, j))
        return connected_cells

    def in_bounds(self, cell):
        """
        Check if a cell is in the map
        :param cell: (x, y) coordinate of the cell
        :return: (boolean)
        """
        x = cell[0]
        y = cell[1]
        return (0 <= x < self.size) and (0 <= y < self.size)

    # Print map on console
    def print_map(self):
        print(self.map)

    # Draw map on canvas
    def draw_map(self, canvas):
        # Determine the width of each cell
        width = FRAME_WIDTH / self.size
        for x in range(0, self.size):
            for y in range(0, self.size):
                # Draw first and last cell
                if (x == 0 and y == 0) or (x == (self.size - 1) and y == (self.size - 1)):
                    canvas.draw_polygon([(x * width, y * width), ((x + 1) * width, y * width),
                                         ((x + 1) * width, (y + 1) * width), ((x * width), (y + 1) * width)], 1,
                                        "Black", "Red")
                # Draw other cells
                else:
                    if (x, y) in self.solved_path[2]:
                        canvas.draw_polygon([(x * width, y * width), ((x + 1) * width, y * width),
                                             ((x + 1) * width, (y + 1) * width), ((x * width), (y + 1) * width)], 1,
                                            "Black", "Yellow")
                    else:
                        if self.map[x, y] == 0:
                            canvas.draw_polygon([(x * width, y * width), ((x + 1) * width, y * width),
                                                 ((x + 1) * width, (y + 1) * width), ((x * width), (y + 1) * width)], 1,
                                                "Black", "White")
                        else:
                            canvas.draw_polygon([(x * width, y * width), ((x + 1) * width, y * width),
                                                 ((x + 1) * width, (y + 1) * width), ((x * width), (y + 1) * width)], 1,
                                                "Black", "#754C24")


class Solution:
    def __init__(self, a_map):
        self.a_map = a_map
        self.time = 0
        self.result = "N/A"
        self.start_position = (0, 0)
        self.end_position = (a_map.size - 1, a_map.size - 1)

    def build_path(self, path_dictionary):
        """
        Build a path (list) from a dictionary of parent cell -> child cell
        :param path_dictionary: (dic) (child.x, child,y) -> (parent.x, parent.y) Child:key, Parent:value
        :return: list of path from start to finish
        """
        path = []
        current = path_dictionary[self.end_position]
        while current!=(0,0):
            path += (current,)
            current = path_dictionary[current]
        return path[::-1]

    def dfs(self):
        """
        Find path using Depth First Search
        :return: list of status and path (if found)
        """
        stack = [self.start_position]
        visited = set()
        parentCell = {}

        while stack:
            cell = stack.pop()
            if cell == self.end_position:
                path = self.build_path(parentCell)
                return [PATH_FOUND, len(path), path]

            for child in self.a_map.connected_cells(cell):
                if child not in visited:
                    parentCell[child] = cell
                    stack.append(child)
                    visited.add(child)

        return [PATH_NOT_FOUND, "N/A", []]


def generate_map():
    global current_map
    current_map = Map(int(input_size.get_text()), float(input_probability.get_text()))
    return


def draw_handler(canvas):
    current_map.draw_map(canvas)
    return


def input_handler():
    return

def solve_with_dfs():
    global current_map
    current_map.solved_path = Solution(current_map).dfs()
    update()

def update():
    status.set_text("STATUS: " + current_map.solved_path[0])
    path_length.set_text("PATH LENGTH: " + str(current_map.solved_path[1]))


current_map = Map(DEFAULT_SIZE, DEFAULT_PROBABILITY)

frame = simplegui.create_frame('Assignment 1', FRAME_WIDTH, FRAME_WIDTH)
frame.add_button("Generate Map", generate_map, 100)
frame.set_draw_handler(draw_handler)
input_size = frame.add_input('Size', input_handler, 50)
input_size.set_text(str(DEFAULT_SIZE))
input_probability = frame.add_input("Probability", input_handler, 50)
input_probability.set_text(str(DEFAULT_PROBABILITY))

# Solve with
frame.add_label("")
frame.add_label("Algorithm")
frame.add_button("DFS", solve_with_dfs, 100)

# Display status
frame.add_label("")
status = frame.add_label("STATUS: " + current_map.solved_path[0])
path_length = frame.add_label("PATH LENGTH: " + str(current_map.solved_path[1]))


frame.start()

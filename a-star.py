import tkinter as tk
import time

width = 800
spalten = 20
breite = width // spalten

black = 'black'
green = 'spring green'
red = 'firebrick3'
blue = 'cyan2'
pink = 'hot pink'
orange = 'orange'

root = tk.Tk()
root.geometry('800x800')
root.resizable(width=0, height=0)

c = tk.Canvas(root, bg='white')
c.pack(fill=tk.BOTH, expand=True)


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.pos = [row, col]
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.parent = None
        self.bar = False

    def __repr__(self):
        return str(self.row) + str(self.col)

    def __str__(self):
        return str(self.row) + str(self.col)

    def get_pos(self):
        return self.pos

    def fcost(self):
        return self.g + self.h

    def get_neighbors(self):

        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 and y == 0):
                    continue
                checkX = self.row + x
                checkY = self.col + y

                if checkX >= 0 and checkX < spalten and checkY >= 0 and checkY < spalten:
                    self.neighbors.append(Node(checkX, checkY))

                for i in self.neighbors:
                    if i.__repr__() in barriers.__repr__():
                        i.bar = True

        return self.neighbors

    def draw_self(self, farbe):
        c.create_rectangle(self.row * breite, self.col * breite, self.row * breite + breite, self.col * breite + breite,
                           outline=black, fill=farbe, width=1)


barriers = [Node(10, 3), Node(10, 13), Node(11, 13), Node(9, 13), Node(1, 9), Node(5, 10)]


def draw(openset, closedset, start, end):
    for j in range(0, len(openset)):
        openset[j].draw_self(green)
    for i in range(0, len(closedset)):
        closedset[i].draw_self(red)
    for k in range(0, len(barriers)):
        barriers[k].draw_self(black)
    start.draw_self(orange)
    end.draw_self(orange)
    draw_lines(width)

    root.update()


def make_grid(spalten):
    grid = []
    for i in range(spalten):
        grid.append([])
        for j in range(spalten):
            node = Node(i, j)
            grid[i].append(node)
    return grid


def get_distance(nodeA, nodeB):
    distX = abs(nodeA.col - nodeB.col)
    distY = abs(nodeA.row - nodeB.row)

    if distX > distY:
        return 14 * distY + 10 * (distX - distY)

    return 14 * distX + 10 * (distY - distX)


def finished(path, start, end):
    for i in path:
        i.draw_self(blue)
        start.draw_self(orange)
        end.draw_self(orange)


def zurückverfolgen(start, end):
    path = []
    temp = end.parent
    while temp is not start:
        path.append(temp)
        temp = temp.parent

    finished(path, start, end)


def astar():
    start = Node(10, 1)
    start.parent = start
    end = Node(10, 14)
    openset = []
    closedset = []
    openset.append(start)

    while len(openset) > 0:
        current_node = openset[0]
        current_index = 0

        for index, item in enumerate(openset):
            if item.fcost() < current_node.fcost() or item.fcost() == current_node.fcost():
                if item.h < current_node.h:
                    current_node = item
                    current_index = index

        openset.pop(current_index)
        closedset.append(current_node)

        if current_node.__repr__() == end.__repr__():
            end.parent = current_node.parent
            zurückverfolgen(start, end)
            return

        for neighbor in current_node.get_neighbors():

            if neighbor.bar == True or neighbor.__repr__() in closedset.__repr__():
                continue

            newCost = current_node.g + get_distance(current_node, start)

            if newCost < neighbor.g or neighbor.__repr__() not in openset.__repr__():

                neighbor.g = get_distance(current_node, start)
                neighbor.h = get_distance(neighbor, end)

                neighbor.parent = current_node

                if neighbor.__repr__() not in openset.__repr__():
                    openset.append(neighbor)

        draw(openset, closedset, start, end)
        print('position: {}, hcost: {}, gcost: {}, fcost: {}, parent: {}'.format(current_node, current_node.h,
                                                                                 current_node.g, current_node.fcost(),
                                                                                 current_node.parent))
        time.sleep(0.3)


def draw_lines(width):
    c.delete('grid_line')
    for i in range(0, width, breite):
        c.create_line([(i, 0), (i, width)], tag='grid_line')

    for i in range(0, width, breite):
        c.create_line([(0, i), (width, i)], tag='grid_line')


def main(spalten, width):
    draw_lines(width)
    grid = make_grid(spalten)
    astar()
    root.mainloop()


if __name__ == '__main__':
    main(spalten, width)

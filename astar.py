import heapq
import math
from setting import *


class node: #class node

    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.remove = False

        self.g = parent.g + 1 if parent is not None else 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


def remove_node(node): #thay đổi thuộc tính remove của node thành True
    node.remove = True


def pop_node(open_list): #lấy node có f nhỏ nhất trong open_list
    while open_list:
        _, node = heapq.heappop(open_list) 
        if not node.remove: #nếu node không được đánh dấu remove thì trả về node
            return node
    return None


def heuristics(a, b): #tính khoảng cách giữa 2 node
    return math.sqrt((a.position[0] - b.position[0]) ** 2 + abs(a.position[1] - b.position[1]) ** 2)


def a_star(maze, start, end): #tìm đường đi ngắn nhất từ start đến end
    start_node = node(None, start)
    end_node = node(None, end)
    open_list = []
    closed_list = set()

    heapq.heappush(open_list, (0, start_node))

    while open_list:
        current_node = pop_node(open_list)
        if current_node.position == end_node.position: #nếu node hiện tại là node cuối thì trả về đường đi
            path = []
            while current_node.parent is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            path.reverse()
            return path

        closed_list.add(current_node.position)

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: #kiểm tra 4 hướng đi
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] < 0 or node_position[0] >= len(maze) or node_position[1] < 0 or node_position[1] >= len(
                    maze[0]):
                continue

            if maze[node_position[0]][node_position[1]] == '1' :
                continue

            if node_position in closed_list:
                continue
            new_node = node(current_node, node_position)
            new_node.h = heuristics(new_node, end_node)
            new_node.f = new_node.g + new_node.h
            for _, existing_node in open_list:
                if existing_node.position == new_node.position:# kiểm tra xem node đã có trong open_list chưa
                    if existing_node.f <= new_node.f: #nếu node đã có trong open_list và f của node đó nhỏ hơn f của new_node thì không thêm new_node vào open_list
                        break
                    else: #nếu node đã có trong open_list và f của node đó lớn hơn f của new_node thì xóa node đó khỏi open_list và thêm new_node vào open_list
                        remove_node(existing_node)
                        heapq.heappush(open_list, (new_node.f, new_node))
                        break
            else: #nếu node chưa có trong open_list thì thêm new_node vào open_list
                heapq.heappush(open_list, (new_node.f, new_node))
    return None
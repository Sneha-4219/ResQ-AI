import heapq
from collections import deque

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    nodes_explored = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        nodes_explored += 1
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, nodes_explored
            
        r, c = current
        for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                cost = 1 if grid[nr][nc] != 'F' else 100
                tentative_g_score = g_score[current] + cost
                
                if (nr, nc) not in g_score or tentative_g_score < g_score[(nr, nc)]:
                    came_from[(nr, nc)] = current
                    g_score[(nr, nc)] = tentative_g_score
                    f_score = tentative_g_score + heuristic((nr, nc), goal)
                    heapq.heappush(open_set, (f_score, (nr, nc)))
                    
    return [], nodes_explored

def bfs_search(grid, start, goal):
    # Standard BFS using a Deque (Level-Order Traversal)
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    came_from = {start: None}
    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if current == goal:
            path = []
            curr = goal
            while curr != start:
                path.append(curr)
                curr = came_from[curr]
            path.reverse()
            return path, nodes_explored

        r, c = current
        for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
            # BFS doesn't use weighted heuristics, we just block fire completely
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] not in ['#', 'F']:
                if (nr, nc) not in came_from:
                    came_from[(nr, nc)] = current
                    queue.append((nr, nc))

    return [], nodes_explored
import numpy as np
from itertools import combinations
import copy

HORSES = 25
RACE_HORSES = 5
TOP = 3

solution = np.arange(1, HORSES + 1)
np.random.shuffle(solution)
print("ranking:", solution)

def race(positions):
    """
    Given a list of horses, return the relative ranking of those horses.
    """
    ranking = np.zeros(len(solution))
    sorted_positions = sorted(positions, key=lambda x: solution[x])
    ranking[sorted_positions] = np.arange(1, len(sorted_positions) + 1)
    return ranking

def remove_nodes(nodes, nodes_to_remove):
    """
    Remove from list "nodes" all elements present on "nodes_to_remove" and with higher cost
    """
    return [node for node in nodes if not node.exists(nodes_to_remove)]

def remove_ancestors(nodes, ancestors):
    """
    Remove from list "nodes" all elements with same root as "ancestors"
    """
    return [node for node in nodes if not node.has_ancestor(ancestors)]

def objective(node):
    """
    Returns if a node has reached the terminal state (ranking of TOP horses)
    """
    unique, counts = np.unique(np.sum(node.state, axis=0), return_counts=True)
    unique_counts = dict(zip(unique, counts))
    for i in range(1, TOP + 1):
      if unique_counts.get(i,0) > 1:
        return False
    return True

class Node:
    def __init__(self, state = np.eye(HORSES).astype(int).tolist(), steps = []):
      self.state = state
      self.steps = steps
      self.cost = self.cost()

    def __str__(self):
      return f"---------\nsteps: {self.steps}\ncost: {self.cost}"

    def heuristic(self):
      """
      This heuristic consists of:
      - how many horses are still not evaluated;
      - how much bits of information we have.
      """
      if objective(self):
        return 0
      horses_to_evaluate = (HORSES - len(set().union(*self.steps)))
      info_missing = (HORSES*(HORSES+1))/2 - np.sum(self.state)
      return horses_to_evaluate*50 + info_missing

    def cost(self):
      """
      The cost to reach this node is the sum of the depth (num. of races) with the heuristic:
      f(n) = g(n) + h(n)
      """
      # return self.heuristic()
      return len(self.steps) + self.heuristic()

    def successors(self):
      """
      Get all possible nodes from this one (races with combinations of n horses).
      """
      nodes = []
      indices = np.arange(0, len(solution))
      races = combinations(indices, RACE_HORSES)
      races = filter(lambda x: len(set(x)) == RACE_HORSES, races)
      for combination in races:
        steps = copy.deepcopy(self.steps)
        state = copy.deepcopy(self.state)
        ranking = race(combination)
        ranking_indices = np.argsort(ranking)[ranking[np.argsort(ranking)] != 0]
        for point in list(combinations(ranking_indices, 2)):
            state[point[0]][point[1]] = 1
            for i in range(len(state)):
                if state[point[1]][i] == 1:
                    state[point[0]][i] = 1
        steps.append(combination)
        nodes.append(Node(state, steps))
      nodes = sorted(nodes, key=lambda x: x.cost)[:1000]
      return nodes

    def has_ancestor(self, ancestors):
      """
      Returns if this node has the given ancestors (same steps).
      """
      steps = copy.deepcopy(self.steps)
      while len(steps) != 0:
        for ancestor in ancestors:
          if str(steps) == str(ancestor.steps):
            return True
        steps.pop()
      return False

    def exists(self, nodes):
      """
      Returns if this node exists on a given list of nodes (and with a lower cost).
      """
      for node in nodes:
        if str(node.state) == str(self.state) and node.cost < self.cost:
          return True
      return False

def a_star(root, queue = None, visited = None):

    if queue is None and visited is None:
        return a_star(root, [root], [])

    if len(queue) == 0:
        return False

    node = queue.pop(0)

    print(node)

    if objective(node):
      return node

    visited.append(node)

    suc = node.successors()

    # remove successors that already exist on queue or visited and with a higher cost
    suc = remove_nodes(suc, visited)
    suc = remove_nodes(suc, queue)

    # get all nodes from queue and visited that exist in successors
    nodes_to_remove = remove_nodes(visited, suc) + remove_nodes(queue, suc)

    # remove from queue and visited all nodes that exist in successors
    queue = remove_ancestors(queue, nodes_to_remove)
    visited = remove_ancestors(visited, nodes_to_remove)

    # put successors on queue by ascending order of cost
    queue += suc
    queue = sorted(queue, key=lambda x: x.cost)[:100]

    return a_star(root, queue, visited)

root = Node()
solution = a_star(root)

# if solution:
#   print("steps:", solution.steps)
# else:
#   print("no solution")
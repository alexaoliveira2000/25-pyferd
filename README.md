# Lead
Recently, I stumbled upon a video (https://www.youtube.com/watch?v=i-xqRDwpilM) about a problem which apparently is used on job interviews (Google, by instance) - this problem and its solution are shown below. After seeing the mathematical analysis performed by humans, I wondered if a search algorithm could reach the same conclusion. After all, it's a problem about a "minimum no. of actions" to reach a solution, which immediately made me think about "shortest path". I tried to look for some code solutions so I could have some clues where to start (or how to think), but could not find any (just the same old analysis shown on the video). On the paragraphs below, I explain my thought process to solve this problem, and mainly how to process and save inference information (extremely important for this problem).

# The 25 Horses Problem
There are 25 horses among which you need to find out the fastest 3 horses. You can conduct a race among at most 5 to find out their relative speed. At no point, you can find out the actual speed of the horse in a race. Find out the minimum no. of races which are required to get the top 3 horses.

# Mathematical Solution
1. Assume the fastest horses are, from 3rd to 1st: $h_{3}$, $h_{16}$ and $h_{19}$ (this is what we want to find out, but don't have access to);
2. We group the horses into groups of 5 and race each group. This gives us 5 races:

$$
\begin{equation}
\begin{pmatrix}
  5th & 4th & 3rd & 2nd & 1st\\
  h_4 & h_2 & h_1 & h_5 & h_3  \\
  h_9 & h_7 & h_6 & h_8 & h_{10} \\
  h_{11} & h_{15} & h_{12} & h_{14} & h_{11} \\
  h_{17} & h_{20} & h_{18} & h_{16} & h_{19} \\
  h_{24} & h_{23} & h_{21} & h_{25} & h_{22} \\
\end{pmatrix}
\end{equation}
$$

3. We race the winner of each group ($h_3$, $h_{10}$, $h_{11}$, $h_{19}$ and $h_{22}$):

$$
\begin{equation}
\begin{pmatrix}
  5th & 4th & 3rd & 2nd & 1st\\
  h_{11} & h_{22} & h_{3} & h_{10} & h_{19} \\
\end{pmatrix}
\end{equation}
$$

4. We then order each initial group according to this 6th race. We are now sure about the fastest horse ($h_{19}$), but not sure about the 2nd and 3rd:

$$
\begin{equation}
\begin{pmatrix}
  5th & 4th & 3rd & 2nd & 1st\\
  h_{17} & h_{20} & h_{18} & h_{16} & h_{19} \\
  h_9 & h_7 & h_6 & h_8 & h_{10} \\
  h_4 & h_2 & h_1 & h_5 & h_3  \\
  h_{24} & h_{23} & h_{21} & h_{25} & h_{22} \\
  h_{11} & h_{15} & h_{12} & h_{14} & h_{11} \\
\end{pmatrix}
\end{equation}
$$

5. From all 25 horses, the ones who can be overall 2nd or 3rd are:
- the 2nd or 3rd from the first group (the group that has the fastest horse overall);
- the 1st or 2nd from the 2nd group (the group that has the horse placed 2nd in the 6th race);
- the 1st from the 3rd group (the group that has the horse placed 3rd in the 6th race).

$$
\begin{equation}
\begin{pmatrix}
  5th & 4th & 3rd & 2nd & 1st\\
   &  & h_{18} & h_{16} & \\
   &  &  & h_8 & h_{10} \\
   &  &  &  & h_3  \\
   &  &  &  & \\
   &  &  &  & \\
\end{pmatrix}
\end{equation}
$$

6. According to this, we perform a 7th race with horses $h_{18}$, $h_{16}$, $h_{8}$, $h_{10}$ and $h_{3}$, being sure about the top 3:

$$
\begin{equation}
\begin{pmatrix}
  5th & 4th & 3rd & 2nd & 1st\\
  h_{18} & h_{8} & h_{10} & h_{3} & h_{16} \\
\end{pmatrix}
\end{equation}
$$

7. Overall top ranking:

$$
\begin{equation}
\begin{pmatrix}
  3rd & 2nd & 1st\\
  h_{3} & h_{16} & h_{19} \\
\end{pmatrix}
\end{equation}
$$

Key thought: from the 6th race, we know that all horses on groups containing the horses placed below 3rd place on the 6th race are never going to be overall top 3.

# Algorithmic Solution

## Solution Representation
We may see that we do not have access to the racing times of each horse, which would simplify the problem to just 5 races (minimum to know the racing times of every horse). Because of this, the problem consists on finding the specific ranking of at least the top 3 horses. In other words, its about finding the right sorting. According to this, we can say that a "solution" is given by:
```py
HORSES = 25

solution = np.arange(1, HORSES + 1)
np.random.shuffle(solution)

# solution = [25  5  7  2 11  1 18  9 10 14 13 24 17  3 12 21 22 19 23  8  4 16 15  6 20]
```

This random solution means that the horse no. 1 was placed 25th, horse no. 2 was placed 5th, etc.

## Race Representation

When performing a race with 5 horses, we get a partial ranking from 1st to 5th:
```py
def race(positions):
    """
    Given a list of horses, return the relative ranking of those horses.
    """
    ranking = np.zeros(len(solution))
    sorted_positions = sorted(positions, key=lambda x: solution[x])
    ranking[sorted_positions] = np.arange(1, len(sorted_positions) + 1)
    return ranking

ranking = race([0, 1, 2, 3, 4])
# ranking = [5. 2. 3. 1. 4. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
```

Considering $t_k$ as the time of horse no. $k$, we can say that $t_1 > t_5 > t_3 > t_2 > t_4$. Here, we must gather all possible bit of information there is, which can be difficult to see at first:
$t_2 > t_4$, $t_3  > t_2$, $t_5 > t_3$, $t_1 > t_5$, $t_3 > t_4$, $t_5 > t_4$, $t_1 > t_4$, $t_5 > t_2$, $t_1 > t_2$ and $t_1 > t_3$. Therefore, given a race with n horses, there is - at least - $C^n_2$ bits of information. Why do I say at least? because this only applies to the first race, where we cannot infer additional information.

## State Representation and Inference
Let's look at a simple example with just 3 horses. If I say that $t_1 > t_2$ and $t_2 > t_3$, I can immediately infer that $t_1 > t_3$, not having, at all, to compare through a new race which one is faster. As you can see (mainly through mathematical analysis), inference is the key to solve this problem with the minimum amount of races. Therefore, we must save all information regarding if a given horse is faster than another, including our inferences.

The best way to save comparisons between every element is through a matrix (not necessarily symmetrical), where each row and column represents a given horse. We start with an identity matrix (main diagonal full of 1's, and everywhere else full of 0's).

$$
\begin{equation}
\begin{pmatrix}
  1 & 0 & 0  \\
  0 & 1 & 0  \\
  0 & 0 & 1  \\
\end{pmatrix}
\end{equation}
$$

If, by instance, $t_1 > t_2$, then coordinate $(2,1)$ has value 1, indicating that the 2nd horse if faster than the 1st:

$$
\begin{equation}
\begin{pmatrix}
  1 & 0 & 0  \\
  1 & 1 & 0  \\
  0 & 0 & 1  \\
\end{pmatrix}
\end{equation}
$$

If we apply the same process to the race between the 2nd and 3rd horse (where $t_2 > t_3$), we change the point $(3,2)$:

$$
\begin{equation}
\begin{pmatrix}
  1 & 0 & 0  \\
  1 & 1 & 0  \\
  0 & 1 & 1  \\
\end{pmatrix}
\end{equation}
$$

Now for the inference part, because we just changed the 2nd column of the matrix (indicating that this horse - no. 3 - is faster), we can also change every column where on the 2nd row there is a 1. The logic here is: the 3rd horse is faster than the 2nd, so we can also say that the 3rd horse is faster than any ones that horse no. 2 beat (indicated by value 1 on the 2nd row). From here, we can infer the following:

$$
\begin{equation}
\begin{pmatrix}
  1 & 0 & 0  \\
  1 & 1 & 0  \\
  1 & 1 & 1  \\
\end{pmatrix}
\end{equation}
$$

This inference is performed when calculating the successors of a state (all possible states after a race):

```py
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
            # inference
            for i in range(len(state)):
                if state[point[1]][i] == 1:
                    state[point[0]][i] = 1
        steps.append(combination)
        nodes.append(Node(state, steps))
      nodes = sorted(nodes, key=lambda x: x.cost)[:1000]
      return nodes
```

The original problem states that we can perform races between 2 and 5 horses, but we can easily demonstrate that performing a race between $n$ horses always gives us more information that performing a race between $n-1$ horses: as stated on the "Race Representation" section, all bits of information we gain performing a race with $n$ horses is $C^n_2$, which is always higher than $C^{n-1}_2$ (assuming $n>2$). On this problem we always perform races with the maximum no. of horses allowed, because it means maximum information gain.

## Objective Function

At any given state (matrix), we can see the ranking of each horse by summing each column:

$$
\begin{equation}
\begin{pmatrix}
  3 & 2 & 1 
\end{pmatrix}
\end{equation}
$$

Initially we admit that every horse is on the 1st place (because of the identity matrix), but once there's only one horse on the 1st place, we are certain about which one is the fastest. The same applies for all other rankings.

Now that we have a state representation, an objective function can be created, indicating if a node is a terminal one (i.e., if we are certain about the top ranking):

```py
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
```

## Search algorithm
### BFS
For a problem with few horses (about 5 or so), BFS can be the best search algorithm because the minimum amount of races we must perform are about 2 or 3, if we race 3 horses at a time. This means that the solution is on depth 2 or 3, and all possible states can be stored and processed by our computer. BFS always guarantees that we find the best solution. However, once we get to a problem with 25 horses and a minimum solution on depth 7 (proven mathematically), we just cannot search every possible state. If we have 25 horses, then we can perform $C^{25}_5 = 53130$ different races with 5 horses. As the tree grows exponentially, just on level 7 we have about $53130^7 \approx 10^{33}$ (1 decillion) states.

### DFS
We could also think about DFS, which searches in depth until finding a solution. This algorithm is extremely fast finding a solution, but with many more races than needed (which is not what we're looking for). We can apply a threshold on the maximum depth it searches, but we have to know the minimum solution depth, besides possibly taking longer than BFS.

### $A^*$
The previous search algorithms are also called "blind", because all given states have the same relevance (a given state is no more relevant than any other, only if it reached the solution!). For this to work, we must select those states which are theoretically closer to the solution, and this can be done using an algorithm such as $A^*$, where we analyse each state and give it a value according to it. The states we select are based on this cost, slowly but surely walking on the right direction towards the solution. By the way, this algorithm does not guarantee the minimum solution, but rather a mix between a fast and near optimal solution. This is done through an heuristic.

As was said above, each state has an associated cost (a positive number). States with a low cost (near 0) are what we're looking for. Cost - $f(n)$ - is typically represented as the follwing function:

$$
\begin{equation}
f(n) = g(n) + h(n)
\end{equation}
$$

where $n$ is a node (or state), $g(n)$ is the "actual cost" function (aka depth, or no. of races performed so far) and $h(n)$ is the heuristic (custom function where we evaluate the state, with values near 0 indicating we're close to the solution and vice-versa).

By this function, we can see that initially $g(n)$ has a null value (because we did not perform any race) and $h(n)$ has the maximum value (because we could not be any further away from the solution). By performing races and gathering information about the state, $g(n)$ increases and $h(n)$ decreases, and so $A^*$ naturally pays attention to the no. of steps performed - $g(n)$ - and what is the "gain" in information performed by each step - $h(n)$.

The heuristic has in account the following insights:
- We must perform at least one race with every horse (because anyone of them could be on the top ranking);
- States with more 1's mean states with more information, therefore being closer to the solution.

```py
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
```

You may have noticed that we give 50 times more importance to evaluating every horse than the information we're missing, which is the same logic on the mathematical analysis. If this importance is ignored, the algorithm typically uses one horse from the previous race, in order to create some kind of "connection" between the horses. We know that that "connection" is made on the 6th race on the original solution, which cannot be seen ahead of time by the algorithm (hence focusing initially on racing every possible horse).

# Parameters
On a final note, you can control 3 parameters on the provided code regarding the specific problem you want to solve:
|Parameter|Description|Default Value|
|---|---|---|
|HORSES|Total number of horses|25|
|RACE_HORSES|Maximum number of horses per race|5|
|TOP|What top ranking positions we want|3

# Additional Analysis
For some parameters, the minimum solution can be dependant of the solution (or chosen horses), where it is impossible to know which horses to choose because of a lack of information.
If we are trying, by instance, to solve this problem with the following parameters: HORSES = 3, RACE_HORSES = 2 and TOP = 3, the minimum races we must perform can be 2 or 3, depending on which horses we choose for the 2nd race:

Assuming $t_1 > t_2 > t_3$:

- First hypothesis (2 races):
1. Race horse 1 and 2 --> $t_1 > t_2$
2. Race horse 2 and 3 --> $t_2 > t_3$
3. Infer --> $t_1 > t_3$
4. Solution --> $t_1 > t_2 > t_3$

- Second hypothesis (2 races):
1. Race horse 1 and 2 --> $t_1 > t_2$
2. Race horse 1 and 3 --> $t_1 > t_3$
3. Race horse 2 and 3 --> $t_2 > t_3$
4. Solution --> $t_1 > t_2 > t_3$

For the orginial problem however, the solution is always 7 races.

# Output
```py
ranking: [11 17 13 19  1  4  7 10 18 20  2 21 24 25 14  3 22 23 12  9  5 16  8 15 6]
steps: [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9), (10, 11, 12, 13, 14), (15, 16, 17, 18, 19), (20, 21, 22, 23, 24), (4, 5, 10, 15, 20), (0, 6, 14, 19, 20)]
```

from collections import deque
import graph_data


class PermutationSolver:
    def __init__(self, graph):
        self.graph = graph

    def sjt_permutations(self, n):
        # Implement the SJT algorithm here
        # Initialize variables for SJT
        perm = list(range(1, n + 1))
        direction = [-1] * n  # -1 means left, +1 means right

        def find_mobile():
            mobile = -1
            for i in range(n):
                if (i + direction[i] >= 0 and i + direction[i] < n and
                        perm[i] > perm[i + direction[i]] and
                        (mobile == -1 or perm[i] > perm[mobile])):
                    mobile = i
            return mobile

        permutations = []
        while True:
            permutations.append(perm[:])
            mobile = find_mobile()
            if mobile == -1:
                break  # No more mobile elements, all permutations generated

            # Swap the mobile element in its direction
            swap_index = mobile + direction[mobile]
            perm[mobile], perm[swap_index] = perm[swap_index], perm[mobile]
            direction[mobile], direction[swap_index] = direction[swap_index], direction[mobile]

            # Reverse direction of all larger elements
            for i in range(n):
                if perm[i] > perm[swap_index]:
                    direction[i] = -direction[i]

        return permutations

    def is_hamiltonian_cycle(self, permutation):
        # Check if the permutation forms a Hamiltonian cycle in the graph
        permutation = [0] + permutation + [len(self.graph) - 1]
        for i in range(len(permutation) - 1):
            if permutation[i+1] not in self.graph[permutation[i]][1]:
                return False
        return True

    def find_hamiltonian_cycles(self):
        n = len(self.graph) - 2
        permutations = self.sjt_permutations(n)
        cycles = []

        for perm in permutations:
            if self.is_hamiltonian_cycle(perm):
                print("Hamiltonian cycle found:", perm)
                cycles.append([0] + perm + [len(self.graph) - 1])

        if cycles:
            return cycles
        else:
            print("-1 or False: No valid Hamiltonian cycle exists")
            return -1

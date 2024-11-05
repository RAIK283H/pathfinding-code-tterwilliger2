
class CliqueFinder:
    def __init__(self, graph):
        self.graph = graph
        self.nodes = list(range(1, len(graph) - 1))  # Exclude Start (0) and Exit (len(graph) - 1)
        self.largest_clique = []

    def is_clique(self, subset):
        """Check if a subset of nodes forms a clique in the graph."""
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                if subset[j] not in self.graph[subset[i]]:
                    return False
        print("Clique found:", subset)  # Debugging statement
        return True

    def find_subsets(self, subset, index):
        """Recursively generate subsets of nodes and check for the largest clique."""
        if index == len(self.nodes):
            if self.is_clique(subset) and len(subset) > len(self.largest_clique):
                self.largest_clique = subset[:]
            return

        # Include the current node in the subset
        subset.append(self.nodes[index])
        self.find_subsets(subset, index + 1)

        # Exclude the current node from the subset
        subset.pop()
        self.find_subsets(subset, index + 1)

    def find_largest_clique(self):
        """Find and return the largest clique."""
        self.find_subsets([], 0)
        return self.largest_clique

"""Cache of tree implementation."""

from bdc.tree import Tree


class Cache:
    """Tree cache."""

    def __init__(self):
        """Initialization."""
        self.nodes = {}
        self.new_nodes = []  # Nodes without node_id

    def load(self, node_id: int, tree: Tree):
        """Load node from tree."""
        if node_id in self.nodes:
            return

        # crete node copy
        new_node = tree.get_node_copy(node_id)
        self.nodes[new_node.data.node_id] = new_node

        # restore node connections and is_deleted attribute
        parent_id = tree.get_parent_id(node_id)
        if parent_id in self.nodes:
            parent = self.nodes[parent_id]
            new_node.data.is_deleted = parent.data.is_deleted
            parent.append_child(new_node)

    def save(self, tree: Tree):
        """Save cache to tree."""
        raise NotImplementedError

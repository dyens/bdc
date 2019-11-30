"""Tree of nodes implementation."""

from typing import (
    Optional,
    Union,
)

from bdc.node import Node


class Tree:
    """Tree of nodes.

    It is simple root node with indexing.

    Example:
        tree = Tree()
        root = tree.add_root('root')
        node1 = tree.add_to_parent('node1', root)
        node2 = tree.add_to_parent('node2', node1)

    """

    def __init__(self):
        """Tree initialization."""
        self.nodes = {}
        self._node_index = 0

    def add_root(self, node_value: str) -> Node:
        """Add root."""
        if self.nodes or self._node_index != 0:
            raise RuntimeError('Tree already have root node')
        return self._create_new_node(node_value)

    def add_to_parent(self, node_value: str, parent: Union[Node, int]) -> Node:
        """Add node to parent."""
        if isinstance(parent, Node):
            parent_index = parent.node_id
        else:
            parent_index = parent

        try:
            tree_parent = self.nodes[parent_index]
        except KeyError:
            raise ValueError(
                '{parent_index} not found'.format(parent_index=parent_index),
            )
        new_node = self._create_new_node(node_value)
        tree_parent.append_child(new_node)
        return new_node

    def get(self, node_id: int) -> Optional[Node]:
        """Get node by node_id."""
        return self.nodes.get(node_id)

    def get_node_copy(self, node_id: int) -> Node:
        """Get node simple copy."""
        node = self.nodes[node_id]
        return node.copy_simple()

    def get_parent_id(self, node_id: int) -> int:
        """Get node parent_id."""
        return self.nodes[node_id].data.parent_id

    def delete(self, node: Union[Node, int]):
        """Delete node from tree."""
        if isinstance(node, Node):
            tree_node = node
        else:
            tree_node = self.get(node)
            if tree_node is None:
                raise ValueError('Unknown node id')
        tree_node.delete()

    def _create_new_node(self, node_value: str) -> Node:
        """Create new node and add it to index."""
        new_node = Node(node_value)
        new_node.node_id = self._node_index
        self._node_index += 1
        self.nodes[new_node.node_id] = new_node
        return new_node

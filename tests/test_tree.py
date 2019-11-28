import pytest

from bdc.node import Node
from bdc.tree import Tree


class TestTree:
    """Tree testing."""

    def test_add_root(self):
        """Test add root."""
        tree = Tree()
        new_node = tree.add_root('val1')
        assert len(tree.nodes) == 1
        assert tree.nodes[0] == new_node
        assert tree.nodes[0].value == 'val1'
        assert tree.nodes[0].is_deleted is False
        assert tree.nodes[0].node_id == 0
        assert tree.nodes[0].parent is None

    def test_add_root_fail_double_add(self):
        """Test add root.

        case: double add.
        """
        tree = Tree()
        tree.add_root('val1')
        with pytest.raises(RuntimeError):
            tree.add_root('val2')

    def test_to_parent(self):
        """Test add to parent."""
        tree = Tree()
        root = tree.add_root('val1')
        child1 = tree.add_to_parent('val2', root)
        child2 = tree.add_to_parent('val3', child1.node_id)

        assert root.node_id == 0
        assert child1.node_id == 1
        assert child2.node_id == 2

        assert len(tree.nodes) == 3
        assert child2.parent == child1
        assert child1.childs == [child2]

        assert child1.parent == root
        assert root.childs == [child1]

    def test_to_parent_fail_unknown_parent(self):
        """Test add to parent fail.

        case: unknown parent.
        """
        tree = Tree()
        tree.add_root('val1')
        with pytest.raises(ValueError):
            tree.add_to_parent('val2', 3)
        unknown_node = Node('val2')
        unknown_node._node_id = 3
        with pytest.raises(ValueError):
            tree.add_to_parent('val2', unknown_node)

    def test_get(self):
        """Test get node."""
        tree = Tree()
        root = tree.add_root('val1')
        assert tree.get(0) == root
        with pytest.raises(KeyError):
            tree.get(1)

    def test_delete(self):
        """Test delete node."""
        tree = Tree()
        root = tree.add_root('val1')
        child1 = tree.add_to_parent('val2', root)
        child2 = tree.add_to_parent('val3', child1.node_id)
        tree.delete(child1)
        assert root.is_deleted is False
        assert child1.is_deleted is True
        assert child2.is_deleted is True

    def test_delete_by_index(self):
        """Test delete node by index."""
        tree = Tree()
        root = tree.add_root('val1')
        child1 = tree.add_to_parent('val2', root)
        child2 = tree.add_to_parent('val3', child1.node_id)
        tree.delete(child1.node_id)
        assert root.is_deleted is False
        assert child1.is_deleted is True
        assert child2.is_deleted is True

import pytest

from bdc.db import DB
from bdc.node import Node


class TestDB:
    """DB testing."""

    def test_add_root(self):
        """Test add root."""
        db = DB()
        new_node = db.add_root('val1')
        assert len(db.nodes) == 1
        assert db.nodes[0] == new_node
        assert db.nodes[0].value == 'val1'
        assert db.nodes[0].is_deleted is False
        assert db.nodes[0].db_id == 0
        assert db.nodes[0].parent is None

    def test_add_root_fail_double_add(self):
        """Test add root.

        case: double add.
        """
        db = DB()
        db.add_root('val1')
        with pytest.raises(RuntimeError):
            db.add_root('val2')

    def test_to_parent(self):
        """Test add to parent."""
        db = DB()
        root = db.add_root('val1')
        child1 = db.add_to_parent(root, 'val2')
        child2 = db.add_to_parent(child1.db_id, 'val3', is_deleted=True)

        assert child1.is_deleted is False
        assert child2.is_deleted is True

        assert root.db_id == 0
        assert child1.db_id == 1
        assert child2.db_id == 2

        assert len(db.nodes) == 3
        assert child2.parent == child1
        assert child1.childs == [child2]

        assert child1.parent == root
        assert root.childs == [child1]

    def test_to_parent_fail_unknown_parent(self):
        """Test add to parent fail.

        case: unknown parent.
        """
        db = DB()
        db.add_root('val1')
        with pytest.raises(ValueError):
            db.add_to_parent(3, 'val2')
        unknown_node = Node('val2')
        unknown_node._db_id = 3
        with pytest.raises(ValueError):
            db.add_to_parent(unknown_node, 'val2')

    def test_get(self):
        """Test get node."""
        db = DB()
        root = db.add_root('val1')
        assert db.get(0) == root
        assert db.get(1) is None

    def test_get_node_params(self):
        """Test get node params."""
        db = DB()
        root = db.add_root('val1')
        db.add_to_parent(root, 'val2', is_deleted=True)
        params = db.get_node_params(1)

        assert params == {
            'db_id': 1,
            'value': 'val2',
            'is_deleted': True,
        }

    def test_get_parent_id(self):
        """Test get parent id."""
        db = DB()
        root = db.add_root('val1')
        db.add_to_parent(root, 'val2', is_deleted=True)
        parent_id = db.get_parent_id(1)
        assert parent_id == 0

        parent_id = db.get_parent_id(0)
        assert parent_id is None

        with pytest.raises(KeyError):
            parent_id = db.get_parent_id(4)

    def test_get_children_ids(self):
        """Test get children ids."""
        db = DB()
        root = db.add_root('val1')
        db.add_to_parent(root, 'val2')
        db.add_to_parent(root, 'val3')

        children_ids = db.get_children_ids(0)
        assert children_ids == [1, 2]

    def test_update_node(self):
        """Test update node."""
        db = DB()
        root = db.add_root('val1')
        child = db.add_to_parent(root, 'val2')
        child2 = db.add_to_parent(child, 'val3')

        new_value = 'val4'
        db.update_node(
            child.db_id,
            new_value,
            is_deleted=True,
        )
        assert child.value == new_value
        assert child.is_deleted is True
        assert child2.is_deleted is True

    def test_create_new_node(self):
        """Test create new node."""
        db = DB()
        new_node = db.create_new_node('val1', is_deleted=False)
        assert new_node.value == 'val1'
        assert new_node.is_deleted is False
        assert new_node.parent is None
        assert db.nodes == {0: new_node}
        assert db._node_index == 1

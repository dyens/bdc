import pytest

from bdc.node import Node


class TestNode:
    """Node Testing."""

    @staticmethod
    @pytest.fixture
    def new_node():
        """Simple node fixture."""
        db_id = 0

        def _create_node():
            """Create new node."""
            nonlocal db_id
            db_id += 1
            return Node('val{db_id}'.format(db_id=db_id))
        return _create_node

    def test_init(self, new_node):
        """Testing node initialization."""
        node = new_node()
        assert node.value == 'val1'
        assert node.is_deleted is False
        assert node.db_id is None
        assert not node.children
        assert node.parent is None

    def test_append_child(self, new_node):
        """Testing append child."""
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        assert parent.children == [child]
        assert child.parent == parent

    def test_append_child_fail_double_append(self, new_node):
        """Testing append child.

        case: double append.
        """
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        with pytest.raises(ValueError):
            parent.append_child(child)

    def test_all_children(self, new_node):
        """Test all children."""
        grand_parent = new_node()
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        grand_parent.append_child(parent)

        assert list(grand_parent.all_children) == [parent, child]

    def test_delete(self, new_node):
        """Test delete."""
        grand_parent = new_node()
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        grand_parent.append_child(parent)

        grand_parent.delete()
        assert grand_parent.is_deleted is True
        assert parent.is_deleted is True
        assert child.is_deleted is True

    def test_set_parent(self, new_node):
        """Testing set parent."""
        parent = new_node()
        child = new_node()
        child.set_parent(parent)
        assert child.parent == parent

    def test_set_parent_deleted(self, new_node):
        """Testing set parent.

        case: deleted parent. Child should be deleted too.
        """
        parent = new_node()
        parent.is_deleted = True
        child = new_node()
        assert child.is_deleted is False
        child.set_parent(parent)
        assert child.is_deleted is True

    def test_set_parent_fail_double_setting(self, new_node):
        """Testing set parent fail.

        case: double setting.
        """
        parent = new_node()
        child = new_node()
        child.set_parent(parent)
        with pytest.raises(ValueError):
            child.set_parent(parent)

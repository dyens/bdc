from bdc.node import Node
import pytest


class TestNode:
    """Node Testing."""

    @staticmethod
    @pytest.fixture
    def new_node():
        """Simple node fixture."""
        node_id = 0
        def _create_node():
            """Create new node."""
            nonlocal node_id
            node_id += 1
            return Node('val{node_id}'.format(node_id=node_id))
        return _create_node

    def test_init(self, new_node):
        """Testing node initialization."""
        node = new_node()
        assert node.value == 'val1'
        assert node._is_deleted is False
        assert node._node_id is None
        assert node._childs == []
        assert node._parent is None


    def test__set_parent(self, new_node):
        """Testing set parent."""
        parent = new_node()
        child = new_node()
        child._set_parent(parent)
        assert child._parent == parent

    def test__set_parent_fail_double_setting(self, new_node):
        """Testing set parent fail.

        case: double setting.
        """
        parent = new_node()
        child = new_node()
        child._set_parent(parent)
        with pytest.raises(ValueError):
            child._set_parent(parent)

    def test_append_child(self, new_node):
        """Testing append child."""
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        assert parent._childs == [child]
        assert child._parent == parent

    def test_append_child_fail_double_append(self, new_node):
        """Testing append child.

        case: double append.
        """
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        with pytest.raises(ValueError):
            parent.append_child(child)

    def test_all_childs(self, new_node):
        """Test all childs."""
        grand_parent = new_node()
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        grand_parent.append_child(parent)

        assert list(grand_parent.all_childs)== [parent, child]
        

    def test_delete(self, new_node):
        """Test delete."""
        grand_parent = new_node()
        parent = new_node()
        child = new_node()
        parent.append_child(child)
        grand_parent.append_child(parent)

        grand_parent.delete()
        assert grand_parent.is_deleted == True
        assert parent.is_deleted == True
        assert child.is_deleted == True
        

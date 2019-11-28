"""Node implementation."""

class Node:
    """Node.
    
    Every node have parent except root node.
    """

    def __init__(self, value: str):
        """Init a new node."""
        self.value = value

        self._is_deleted = False
        self._node_id = None
        self._childs = []
        self._parent = None

    @property
    def is_deleted(self):
        """Is deleted."""
        return self._is_deleted

    def _set_parent(self, parent: 'Node'):
        """Set parent.

        Tree should be created by append child from root node.
        """
        if self._parent is not None:
            raise ValueError('This node already have parent')
        self._parent = parent

    def append_child(self, child: 'Node'):
        """Add node to child list."""
        child._set_parent(self)
        self._childs.append(child)


    @property
    def all_childs(self):
        """Get all childs recursively."""
        childs = [i for i in self._childs]
        while childs:
            child = childs.pop()
            childs.extend(child._childs)
            yield child

    def delete(self):
        """Delete node."""
        self._is_deleted = True
        for child in self.all_childs:
            child._is_deleted = True

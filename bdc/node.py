"""Node implementation."""

from typing import (
    List,
    Optional,
)


class Node:
    """Node.

    Every node have parent except root node.
    """

    def __init__(self, value: str):
        """Init a new node."""
        self.value = value
        self.node_id = None

        self._is_deleted = False
        self._childs: List['Node'] = []
        self._parent: Optional['Node'] = None

    @property
    def is_deleted(self):
        """Is deleted."""
        return self._is_deleted

    @property
    def parent(self):
        """Parent."""
        return self._parent

    @property
    def childs(self):
        """Childs."""
        return self._childs

    def append_child(self, child: 'Node'):
        """Add node to child list."""
        child._set_parent(self)  # NOQA:WPS437
        self._childs.append(child)

    @property
    def all_childs(self):
        """Get all childs recursively."""
        childs = [child for child in self._childs]
        while childs:
            child = childs.pop()
            childs.extend(child._childs)  # NOQA:WPS437
            yield child

    def delete(self):
        """Delete node."""
        self._is_deleted = True
        for child in self.all_childs:
            child._is_deleted = True  # NOQA:WPS437

    def _set_parent(self, parent: 'Node'):
        """Set parent.

        Tree should be created by append child from root node.
        """
        if self._parent is not None:
            raise ValueError('This node already have parent')
        self._parent = parent

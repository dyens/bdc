"""Node implementation."""

from typing import (
    List,
    Optional,
)


class Node:
    """Node.

    Every node have parent except root node.
    """

    def __init__(
        self,
        value: str,
        db_id: Optional[int] = None,
        is_deleted: bool = False,
    ):
        """Init a new node."""
        self.value = value
        self.is_deleted = is_deleted
        self.db_id = db_id
        self.childs: List['Node'] = []
        self.parent: Optional['Node'] = None

    def append_child(self, child: 'Node'):
        """Add node to child list."""
        child.set_parent(self)  # NOQA:WPS437
        self.childs.append(child)

    @property
    def all_childs(self):
        """Get all childs recursively."""
        childs = [child for child in self.childs]
        while childs:
            child = childs.pop()
            childs.extend(child.childs)  # NOQA:WPS437
            yield child

    def delete(self) -> List['Node']:
        """Delete node.

        Return deleted childs
        """
        deleted_nodes = []
        self.is_deleted = True
        for child in self.all_childs:
            child.is_deleted = True  # NOQA:WPS437
            deleted_nodes.append(child)
        return deleted_nodes

    def set_parent(self, parent: 'Node'):
        """Set parent.

        DB should be created by append child from root node.
        """
        if self.parent is not None:
            raise ValueError('This node already have parent')
        self.parent = parent
        # If parent already deleted child should be deleted too
        if parent.is_deleted:
            self.is_deleted = True


class CNode(Node):
    """Cached node.

    Default node with cache_id.
    """

    def __init__(
        self,
        cache_id: int,
        value: str,
        db_id: Optional[int] = None,
        is_deleted: bool = False,
    ):
        """Init a new node."""
        super().__init__(value, db_id, is_deleted)
        self.cache_id = cache_id

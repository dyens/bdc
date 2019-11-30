"""Node implementation."""

from typing import (
    List,
    Optional,
)

from dataclass import dataclass


@dataclass
class NodeData:
    """Node data."""

    node_id: Optional[int] = None
    value: str
    is_deleted: bool = False


class Node:
    """Node.

    Every node have parent except root node.
    """

    def __init__(
        self,
        value: str,
        node_id: Optional[int] = None,
        is_deleted: bool = False,
    ):
        """Init a new node."""
        self.data = NodeData(
            node_id=node_id,
            value=value,
            is_deleted=is_deleted,
        )
        self.childs: List['Node'] = []
        self.parent: Optional['Node'] = None

    def append_child(self, child: 'Node'):
        """Add node to child list."""
        child._set_parent(self)  # NOQA:WPS437
        self.childs.append(child)

    @property
    def all_childs(self):
        """Get all childs recursively."""
        childs = [child for child in self.childs]
        while childs:
            child = childs.pop()
            childs.extend(child._childs)  # NOQA:WPS437
            yield child

    def delete(self):
        """Delete node."""
        self.data.is_deleted = True
        for child in self.all_childs:
            child.data.is_deleted = True  # NOQA:WPS437

    def copy_simple(self) -> 'Node':
        """Copy node without node connections."""
        return Node(
            node_id=self.data.node_id,
            value=self.data.value,
            is_deleted=self.data.is_deleted,
        )

    def _set_parent(self, parent: 'Node'):
        """Set parent.

        Tree should be created by append child from root node.
        """
        if self.parent is not None:
            raise ValueError('This node already have parent')
        self.parent = parent

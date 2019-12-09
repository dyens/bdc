"""DB of nodes implementation."""

from typing import (
    List,
    Optional,
    Union,
)

from bdc.node import (
    Node,
    NodeParams,
)


class DB:
    """DB of nodes.

    It is simple root node with indexing.

    Example:
        db = DB()
        root = db.add_root('root')
        node1 = db.add_to_parent('node1', root)
        node2 = db.add_to_parent('node2', node1)

    """

    node_cls = Node

    def __init__(self):
        """DB initialization."""
        self.nodes = {}
        self._node_index = 0

    @classmethod
    def default(cls):
        """Create default db with hierarchy = 4.

        0 root
        1   node_1_1
        3     node_2_1
        5       node_3_1
        7         node_4_1
        8         node_4_2
        6       node_3_2
        4     node_2_2
        2   node_1_2
        """
        db = cls()
        root = db.add_root('root')

        node_1_1 = db.add_to_parent(root, 'node_1_1')
        db.add_to_parent(root, 'node_1_2')

        node_2_1 = db.add_to_parent(node_1_1, 'node_2_1')
        db.add_to_parent(node_1_1, 'node_2_2')

        node_3_1 = db.add_to_parent(node_2_1, 'node_3_1')
        db.add_to_parent(node_2_1, 'node_3_2')

        db.add_to_parent(node_3_1, 'node_4_1')
        db.add_to_parent(node_3_1, 'node_4_2')
        return db

    def add_root(self, value: str) -> Node:
        """Add root."""
        if self.nodes or self._node_index != 0:
            raise RuntimeError('DB already have root node')
        return self.create_new_node(value, is_deleted=False)

    def add_to_parent(
        self,
        parent: Union[Node, int],
        value: str,
        is_deleted: bool = False,
    ) -> Node:
        """Add node to parent."""
        if isinstance(parent, Node):
            parent_index = parent.db_id
        else:
            parent_index = parent

        try:
            db_parent = self.nodes[parent_index]
        except KeyError:
            raise ValueError(
                '{parent_index} not found'.format(parent_index=parent_index),
            )
        new_node = self.create_new_node(value, is_deleted)
        db_parent.append_child(new_node)
        return new_node

    def get(self, db_id: int) -> Optional[Node]:
        """Get node by db_id."""
        node: Optional[None] = self.nodes.get(db_id)
        return node  # NOQA: WPS331

    def get_node_params(self, db_id: int) -> NodeParams:
        """Get node simple copy."""
        node = self.nodes[db_id]
        return NodeParams(
            db_id=node.db_id,
            value=node.value,
            is_deleted=node.is_deleted,
        )

    def get_parent_id(self, db_id: int) -> Optional[int]:
        """Get node parent_id."""
        node = self.nodes[db_id]
        parent = node.parent
        if parent:
            parent_id: int = parent.db_id
            return parent_id  # NOQA: WPS331
        return None

    def get_children_ids(self, db_id: int) -> List[int]:
        """Get node parent_id."""
        return [child.db_id for child in self.nodes[db_id].children]

    def update_node(self, db_id: int, value: str, is_deleted: bool) -> Optional[List[Node]]:
        """Update node.

        If node deleted, all children marked as deleted.
        If deleting node func return deleted children.
        """
        node = self.nodes[db_id]
        node.value = value
        # Undeleted operation not exist
        if is_deleted:
            deleted_children: List[Node] = node.delete()
            return deleted_children  # NOQA:WPS331
        return None

    def create_new_node(self, value: str, is_deleted: bool) -> Node:
        """Create new node and add it to index."""
        db_id = self._node_index
        self._node_index += 1
        new_node = self.node_cls(value, db_id, is_deleted)
        self.nodes[db_id] = new_node
        return new_node

"""Cache of db implementation."""

from bdc.db import DB
from bdc.node import CNode


class Cache:
    """DB cache."""

    def __init__(self):
        """Initialization."""
        # Nodes  db index
        self.db_nodes = {}
        # Nodes  cache  index
        self.cache_nodes = {}
        self._cache_index = 0
        super().__init__()

    def delete(self, cache_id: int):
        """Delete nodes from cache."""
        node = self.cache_nodes[cache_id]
        node.delete()

    default_name = 'New Node'

    def add_node(self, parent_cache_id: int) -> CNode:
        """Add new node to parent."""
        parent = self.cache_nodes[parent_cache_id]
        cache_id = self._cache_index
        self._cache_index += 1

        new_node = CNode(
            cache_id=cache_id,
            value=self.default_name,
            db_id=None,
            is_deleted=False,
        )
        parent.append_child(new_node)
        self.cache_nodes[cache_id] = new_node
        return new_node

    def load(self, db_id: int, db: DB):
        """Load node from db."""
        # node already loaded
        if db_id in self.db_nodes:
            return

        # create node copy
        new_node_params = db.get_node_params(db_id)
        db_id = new_node_params['db_id']
        cache_id = self._cache_index
        self._cache_index += 1
        new_node = CNode(cache_id, **new_node_params)
        self.db_nodes[db_id] = new_node
        self.cache_nodes[cache_id] = new_node

        # restore node connections

        # restore parent and is_deleted attribute
        # if parent deleted node should be deleted to
        parent_id = db.get_parent_id(db_id)
        if parent_id in self.db_nodes:
            parent = self.db_nodes[parent_id]
            new_node.is_deleted = parent.is_deleted
            parent.append_child(new_node)

        # restore child connections
        child_ids = db.get_children_ids(db_id)
        for child_id in child_ids:
            if child_id in self.db_nodes:
                child = self.db_nodes[child_id]
                new_node.append_child(child)

    def save(self, db: DB):
        """Save cache to db."""
        # new created nodes appended to the end of dict
        # in python >= 3.6 dicts are ordered
        for _cache_id, node in self.cache_nodes.items():
            db_id = node.db_id
            if db_id:
                db.update_node(
                    db_id,
                    node.value,
                    node.is_deleted,
                )
                continue

            parent = node.parent
            if parent is None:
                raise RuntimeError('In cache all new nodes is subnodes')

            new_node = db.add_to_parent(
                parent.db_id,
                node.value,
                node.is_deleted,
            )
            self.db_nodes[new_node.db_id] = node

"""Cache of db implementation."""

from bdc.db import DB
from bdc.node import (
    CNode,
    NodeParams,
)


class Cache:
    """DB cache."""

    def __init__(self):
        """Initialization."""
        # Nodes  db index
        self.db_nodes = {}
        # Without parent node db_ids
        self.orphans = set()
        # Nodes  cache  index
        self.cache_nodes = {}
        self._cache_index = 0

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

        new_node_params = NodeParams(
            value=self.default_name,
            db_id=None,
            is_deleted=False,
        )

        new_node = CNode(
            cache_id=cache_id,
            node_params=new_node_params,
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
        cache_id = self._cache_index
        self._cache_index += 1
        new_node = CNode(
            cache_id=cache_id,
            node_params=new_node_params,
        )
        self.db_nodes[new_node_params.db_id] = new_node
        self.cache_nodes[cache_id] = new_node

        # restore node connections

        adoptees = []
        for orphan in self.orphans:
            is_child = db.is_child(orphan, db_id)
            if is_child:
                child = self.db_nodes[orphan]
                new_node.append_child(child)
                adoptees.append(orphan)
        self.orphans -= set(adoptees)

        # restore parent and is_deleted attribute
        # if parent deleted node should be deleted to
        parent_id = db.get_parent_id(db_id)
        if parent_id in self.db_nodes:
            parent = self.db_nodes[parent_id]
            parent.append_child(new_node)
            self.orphans.discard(db_id)
            if parent.is_deleted:
                new_node.delete()
        else:
            self.orphans.add(db_id)

    def save(self, db: DB):
        """Save cache to db."""
        # new created nodes appended to the end of dict
        # in python >= 3.6 dicts are ordered
        deleted = []
        for _cache_id, node in self.cache_nodes.items():
            db_id = node.db_id
            if db_id is not None:
                deleted_children = db.update_node(
                    db_id,
                    node.value,
                    node.is_deleted,
                )
                if deleted_children:
                    deleted.extend(deleted_children)
                continue

            parent = node.parent
            if parent is None:
                raise RuntimeError('In cache all new nodes is subnodes')

            new_node = db.add_to_parent(
                parent.db_id,
                node.value,
                node.is_deleted,
            )
            # now new node have db_id
            node.db_id = new_node.db_id
            self.db_nodes[new_node.db_id] = node

        # Case when delete root node.
        # But in cache we have not connection from
        # some subnode to this root.
        # This subnode should be deleted too.
        for db_node in deleted:
            cache_node = self.db_nodes.get(db_node.db_id)
            if cache_node:
                cache_node.delete()

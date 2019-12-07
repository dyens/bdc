import pytest

from bdc.cache import Cache
from bdc.db import DB


class TestCache:
    """Cache testing."""

    @staticmethod
    @pytest.fixture
    def cache():
        """Simple cache fixture.

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
        db = DB.default()
        new_cache = Cache()
        for db_id in db.nodes:
            new_cache.load(db_id, db)
        return new_cache

    def test_delete(self, cache):
        """Test delete."""
        # delete node_2_1
        cache.delete(3)
        # Parent not deleted
        assert cache.cache_nodes[1].is_deleted is False
        # Node with childs deleted
        assert cache.cache_nodes[3].is_deleted is True
        assert cache.cache_nodes[5].is_deleted is True
        assert cache.cache_nodes[7].is_deleted is True

    def test_add_node(self, cache):
        """Test add_node."""
        new_node = cache.add_node(5)
        assert cache.cache_nodes[9] == new_node
        assert new_node.cache_id == 9
        assert new_node.value == Cache.default_name
        assert new_node.is_deleted is False

    def test_load(self):
        """Test load from db."""
        db = DB.default()
        cache = Cache()
        cache.load(5, db)

        m_node = cache.cache_nodes[0]
        assert m_node.value == 'node_3_1'
        assert m_node.parent is None
        assert not m_node.childs

        cache.load(7, db)

        l_node = cache.cache_nodes[1]
        assert l_node.value == 'node_4_1'
        assert l_node.parent is m_node
        assert not l_node.childs
        assert m_node.childs == [l_node]

        cache.load(3, db)

        h_node = cache.cache_nodes[2]
        assert h_node.value == 'node_2_1'
        assert h_node.parent is None
        assert h_node.childs == [m_node]
        assert m_node.parent == h_node

    def test_save(self):
        """Test save to db."""
        db = DB.default()
        cache = Cache()
        cache.load(3, db)
        cache.load(5, db)
        cache.load(7, db)
        cache.add_node(1)
        cache.delete(1)
        cache.cache_nodes[1].value = 'new_value'

        # Cache struct:
        # id del cid value
        # 3  f   0   node_2_1
        # 5  t   1     node_value
        # 7  t   2       node_4_1
        # ?  t   3       New Node

        cache.save(db)
        assert len(cache.db_nodes) == len(cache.cache_nodes)

        new_node = cache.db_nodes[9]
        assert cache.cache_nodes[3] == new_node
        assert new_node.value == 'New Node'

        # DB struct:
        # id del cid value
        # 0  f   ?   root
        # 1  f   ?     node_1_1
        # 3  f   0       node_2_1
        # 5  t   1         node_value
        # 7  t   2           node_4_1
        # 8  t   3           node_4_2
        # 9  t   4           New Node
        # 6  f   ?         node_3_2
        # 4  f   ?       node_2_2
        # 2  f   ?     node_1_2
        node_1_1 = db.nodes[1]
        node_2_1 = db.nodes[3]
        node_3_2 = db.nodes[6]
        node_modified = db.nodes[5]
        node_4_1 = db.nodes[7]
        node_4_2 = db.nodes[8]
        new_node = db.nodes[9]

        assert new_node.is_deleted is True
        assert new_node.value == 'New Node'
        assert not new_node.childs
        assert new_node.parent == node_modified

        assert node_4_1.is_deleted is True
        assert node_4_1.value == 'node_4_1'
        assert not node_4_1.childs
        assert node_4_1.parent == node_modified

        assert node_modified.is_deleted is True
        assert node_modified.value == 'new_value'
        assert set(node_modified.childs) == {node_4_1, node_4_2, new_node}
        assert node_modified.parent == node_2_1

        assert node_2_1.is_deleted is False
        assert node_2_1.value == 'node_2_1'
        assert set(node_2_1.childs) == {node_modified, node_3_2}
        assert node_2_1.parent == node_1_1

    def test_save_update_deleted_childs(self):
        """Test save to db.

        case: auto update deleted childs in cache
        """
        db = DB.default()
        cache = Cache()
        cache.load(3, db)
        cache.load(7, db)
        root_cache = cache.cache_nodes[0]
        child_cache = cache.cache_nodes[1]
        root_db = db.nodes[3]
        child_db = db.nodes[7]
        root_cache.delete()
        cache.save(db)
        assert root_cache.is_deleted is True
        assert root_db.is_deleted is True
        assert child_cache.is_deleted is True
        assert child_db.is_deleted is True


class TestCacheDBInteraction:
    """Cache-db interactions testing.

    DB struct:
    id value
    0  root
    1    node_1_1
    3      node_2_1
    5        node_3_1
    7          node_4_1
    8          node_4_2
    6        node_3_2
    4      node_2_2
    2    node_1_2
    """

    def test_update_value(self):
        """Test update value."""
        db = DB.default()
        cache = Cache()
        cache.load(5, db)
        cache.cache_nodes[0].value = 'new_value'
        cache.save(db)
        assert db.nodes[5].value == 'new_value'

    def test_delete(self):
        """Test delete."""
        db = DB.default()
        cache = Cache()
        cache.load(5, db)
        cache.delete(0)
        cache.save(db)
        assert db.nodes[5].is_deleted is True
        assert db.nodes[7].is_deleted is True
        assert db.nodes[8].is_deleted is True

    def test_new(self):
        """Test new."""
        db = DB.default()
        cache = Cache()
        cache.load(5, db)
        cache.add_node(0)
        cache.save(db)
        assert db.nodes[9].value == Cache.default_name

    def test_new_and_delete_parent(self):
        """Test new and delete parent."""
        db = DB.default()
        cache = Cache()
        cache.load(5, db)
        cache.add_node(0)
        cache.delete(0)
        cache.save(db)
        assert cache.cache_nodes[0].is_deleted is True
        assert cache.cache_nodes[1].is_deleted is True
        assert db.nodes[5].is_deleted is True
        assert db.nodes[7].is_deleted is True
        assert db.nodes[8].is_deleted is True
        assert db.nodes[9].is_deleted is True

    def test_new_and_delete_gp(self):
        """Test add grand parent, child. Add new to child and delete gp."""
        db = DB.default()
        cache = Cache()
        cache.load(1, db)
        cache.load(5, db)
        cache.add_node(1)
        cache.delete(0)
        assert cache.cache_nodes[1].is_deleted is False
        assert cache.cache_nodes[2].is_deleted is False
        cache.save(db)
        assert cache.cache_nodes[0].is_deleted is True
        # child and new node deleted after load too.
        assert cache.cache_nodes[1].is_deleted is True
        assert cache.cache_nodes[2].is_deleted is True
        assert db.nodes[1].is_deleted is True
        assert db.nodes[3].is_deleted is True
        assert db.nodes[5].is_deleted is True
        assert db.nodes[7].is_deleted is True
        assert db.nodes[8].is_deleted is True
        assert db.nodes[6].is_deleted is True
        assert db.nodes[4].is_deleted is True

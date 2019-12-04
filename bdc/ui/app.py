
from PyQt5 import QtWidgets

from bdc.ui import design
from bdc.ui.qcache import QCache
from bdc.ui.qdb import QDB


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """Main ui application."""

    def __init__(self):
        """Initialization."""
        super().__init__()
        self.setupUi(self)

        self.setup_db_view()
        self.setup_cache_view()

        self.load_to_cache_button.clicked.connect(self.load_to_cache)
        self.reset_cache_button.clicked.connect(self.reset)
        self.remove_node_button.clicked.connect(self.remove_node)
        self.edit_node_button.clicked.connect(self.edit_node)
        self.add_node_button.clicked.connect(self.add_node)
        self.apply_cache_button.clicked.connect(self.apply_cache)

    def setup_db_view(self):
        """Setuping db view."""
        self.db_model = QDB()
        self.db_model.update()
        self.db_view.setModel(self.db_model)
        self.db_view.expandAll()

        # by default db is not editable
        self.db_view.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers,
        )

    def setup_cache_view(self):
        """Setuping cached view."""
        self.cache_model = QCache()
        self.cache_model.update()
        self.cache_view.setModel(self.cache_model)

    def reset(self):
        """Refresh cache and model views."""
        self.setup_cache_view()
        self.setup_db_view()

    def remove_node(self):
        """Remove node."""
        selected = self.cache_view.selectedIndexes()
        if not selected:
            return
        selected = selected[0]
        qnode = self.cache_model.itemFromIndex(selected)
        self.cache_model.cache.delete(qnode.node.cache_id)
        self.cache_model.refresh()
        self.cache_view.expandAll()

    def load_to_cache(self):
        """Load to cache."""
        selected = self.db_view.selectedIndexes()
        if not selected:
            return
        selected = selected[0]
        qnode = self.db_model.itemFromIndex(selected)
        self.cache_model.cache.load(qnode.node.db_id, self.db_model.db)
        self.cache_model.refresh()
        self.cache_view.expandAll()

    def edit_node(self):
        """Edit node."""
        selected = self.cache_view.selectedIndexes()
        if not selected:
            return
        selected = selected[0]
        node = self.cache_model.itemFromIndex(selected)
        self.cache_view.edit(node.index())

    def add_node(self):
        """Add node."""
        selected = self.cache_view.selectedIndexes()
        if not selected:
            return
        selected = selected[0]
        qnode = self.cache_model.itemFromIndex(selected)
        self.cache_model.cache.add_node(qnode.node.cache_id)
        self.cache_model.refresh()
        self.cache_view.expandAll()

    def apply_cache(self):
        """Apply cache to db."""
        self.cache_model.cache.save(self.db_model.db)
        self.db_model.refresh()
        self.db_view.expandAll()

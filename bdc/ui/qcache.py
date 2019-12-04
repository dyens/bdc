
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel

from bdc.cache import Cache
from bdc.ui.qnode import NodeToQNodeMixin


class QCache(QStandardItemModel, NodeToQNodeMixin):
    """QT Cache model view."""

    def __init__(self):
        """Initialization."""
        self.cache = Cache()
        super().__init__()
        self.dataChanged.connect(self.data_changed)

    def data_changed(
        self,
        top_left: QModelIndex,
        bottom_right: QModelIndex,
        roles,
    ):
        """Change node data after editing."""
        qnode = self.itemFromIndex(top_left)
        qnode.node.value = qnode.text()

    def update(self):
        """Update qt items from items."""
        self.node_to_qnode(self.cache.cache_nodes.values())

    def refresh(self):
        """Refresh model."""
        self.clear()
        self.update()

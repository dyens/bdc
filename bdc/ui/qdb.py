from PyQt5.QtGui import QStandardItemModel

from bdc.db import DB
from bdc.ui.qnode import NodeToQNodeMixin


class QDB(QStandardItemModel, NodeToQNodeMixin):
    """QT DB model view."""

    def __init__(self):
        """Initialization."""
        super().__init__()
        self.db = DB.default()

    def update(self):
        """Update qt items from items."""
        self.node_to_qnode(self.db.nodes.values())

    def refresh(self):
        """Refresh model."""
        self.clear()
        self.update()

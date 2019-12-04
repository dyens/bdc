from PyQt5.QtGui import QStandardItemModel

from bdc.db import DB
from bdc.ui.node import NodeToQNodeMixin


class QDB(QStandardItemModel, NodeToQNodeMixin):
    """QT DB model view."""

    def __init__(self):
        """Initialization."""
        self.db = DB.default()
        super().__init__()

    def update(self):
        """Update qt items from items."""
        self.node_to_qnode(self.db.nodes.values())

    def refresh(self):
        """Refresh model."""
        self.clear()
        self.update()

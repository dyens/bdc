from typing import (
    Dict,
    Iterable,
)

from PyQt5.QtGui import (
    QStandardItem,
    QStandardItemModel,
)

from bdc.node import Node


class QNode(QStandardItem):
    """QNode.

    QItem for using in qt app.
    """

    def __init__(self, node: Node):
        """Initialization."""
        self.node = node
        super().__init__(self.node.value)
        if node.is_deleted:
            self.setEditable(False)  # NOQA:WPS425
            self.setEnabled(False)  # NOQA:WPS425


class NodeToQNodeMixin(QStandardItemModel):
    """Mixin for creating QNodes from node list."""

    def node_to_qnode(self, node_list: Iterable[Node]):
        """Create qnodes from node list."""
        loaded_nodes: Dict[Node, QNode] = {}
        to_load = list(node_list)
        while to_load:
            node = to_load.pop()
            if node in loaded_nodes:
                continue
            parent = node.parent
            if parent is not None and parent not in loaded_nodes:
                to_load.append(node)
                to_load.append(parent)
                continue

            if parent is None:
                qnode = QNode(node)
                self.appendRow(qnode)
            else:
                qparent = loaded_nodes[parent]
                qnode = QNode(node)
                qparent.appendRow(qnode)
            loaded_nodes[node] = qnode

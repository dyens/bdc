import sys
from collections.abc import Iterable

from PyQt5 import QtWidgets
from PyQt5.QtGui import (
    QStandardItem,
    QStandardItemModel,
)

from bdc import design


class Item(QStandardItem):
    """UI item."""

    id_counter = 0

    def __init__(self, value: str, childs=None):
        """Initialization."""
        self.value = value
        self.is_deleted = False
        self.__class__.id_counter += 1  # NOQA
        self._id = self.__class__.id_counter
        if childs is None:
            childs = []
        self.childs = childs
        super().__init__(value)

    def appendRow(self, rows):
        """Append row."""
        if not isinstance(rows, Iterable):
            rows = [rows]
        self.childs.extend(rows)
        return super().appendRow(rows)

    def removeRows(self, row, count):
        """Remove rows."""
        assert count == 1  # NOQA
        del self.childs[row:row + count]  # NOQA
        return super().removeRows(row, count)

    def print_tree(self, tab=0):
        """Debugging print ;-)."""
        tabs = ' ' * tab
        print('{tabs}{_id}:{value}'.format(tabs=tabs, _id=self._id, value=self.value,)) # NOQA
        tab += 1
        for child in self.childs:
            child.print_tree(tab)


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """Main ui application."""

    def __init__(self):
        """Initialization."""
        super().__init__()
        self.setupUi(self)
        self.setup_cached_view()

    def setup_cached_view(self):
        """Setuping cached view."""
        self.cache_model = QStandardItemModel()
        self.cache_view.setModel(self.cache_model)

        self.root_item = Item('root')

        items = []
        hierarchy = 0
        while True:
            hierarchy += 1
            if hierarchy == 5:
                break
            if not items:
                for i in range(3):
                    item = Item('%d' % i)
                    items.append(item)
                    self.root_item.appendRow(item)
                continue

            new_items = []
            for item in items:
                for i in range(3):
                    nitem = Item('%s:%d' % (item.value, i))
                    item.appendRow(nitem)
                    new_items.append(nitem)
            items = new_items

        self.cache_model.appendRow(self.root_item)
        self.root_item.print_tree()

        self.cache_view.expandAll()

        # by default tree is not editable
        self.cache_view.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.edit_node_button.clicked.connect(self.edit_node)
        self.add_node_button.clicked.connect(self.add_node)
        self.remove_node_button.clicked.connect(self.remove_node)

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
        node = self.cache_model.itemFromIndex(selected)
        node.appendRow(Item("test"))

        # By default items collapsed for hierarchy > 2
        self.cache_view.expandAll()

    def remove_node(self):
        """Remove node."""
        selected = self.cache_view.selectedIndexes()
        if not selected:
            return
        selected = selected[0]
        self.cache_model.removeRows(selected.row(), 1, selected.parent())


def main():
    """Entry point."""
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

import sys

from PyQt5 import QtWidgets

from bdc.ui.app import App


def main():
    """Entry point."""
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bdc/design.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 378)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setEnabled(True)
        self.centralWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralWidget.setMouseTracking(True)
        self.centralWidget.setAutoFillBackground(False)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 851, 361))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cache_view = QtWidgets.QTreeView(self.horizontalLayoutWidget)
        self.cache_view.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cache_view.setObjectName("cache_view")
        self.verticalLayout.addWidget(self.cache_view)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_node_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_node_button.setMaximumSize(QtCore.QSize(50, 16777215))
        self.add_node_button.setSizeIncrement(QtCore.QSize(0, 0))
        self.add_node_button.setObjectName("add_node_button")
        self.horizontalLayout_2.addWidget(self.add_node_button)
        self.remove_node_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.remove_node_button.setMaximumSize(QtCore.QSize(50, 16777215))
        self.remove_node_button.setObjectName("remove_node_button")
        self.horizontalLayout_2.addWidget(self.remove_node_button)
        self.edit_node_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.edit_node_button.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edit_node_button.setObjectName("edit_node_button")
        self.horizontalLayout_2.addWidget(self.edit_node_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.apply_cache_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.apply_cache_button.setObjectName("apply_cache_button")
        self.horizontalLayout_2.addWidget(self.apply_cache_button)
        self.reset_cache_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.reset_cache_button.setObjectName("reset_cache_button")
        self.horizontalLayout_2.addWidget(self.reset_cache_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.load_to_cache_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.load_to_cache_button.setObjectName("load_to_cache_button")
        self.horizontalLayout.addWidget(self.load_to_cache_button)
        self.model_view = QtWidgets.QTreeView(self.horizontalLayoutWidget)
        self.model_view.setObjectName("model_view")
        self.horizontalLayout.addWidget(self.model_view)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.mainToolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "bdc"))
        self.add_node_button.setText(_translate("MainWindow", "+"))
        self.remove_node_button.setText(_translate("MainWindow", "-"))
        self.edit_node_button.setText(_translate("MainWindow", "a"))
        self.apply_cache_button.setText(_translate("MainWindow", "Apply"))
        self.reset_cache_button.setText(_translate("MainWindow", "Reset"))
        self.load_to_cache_button.setText(_translate("MainWindow", "<<"))



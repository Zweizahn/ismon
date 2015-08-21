import sys
from PyQt4 import QtGui, QtCore
from globals import *
from globals import __version__
from globals import __author__
from globals import __last_changed__


############## Classes for GUI
class AboutWindow(QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent=parent)
        path = sys.argv[0].split('\\')
        name = path[len(path) - 1]
        text = "     Script name & version: " + name + __version__ + '\n' + __author__ + '\n' + __last_changed__ + '\n\n'
        text = text + """
    Script uses Qt toolkit www.qt.io with the LGPL.
    """
        self.setText(text)
        self.setGeometry(500, 500, 250, 150)
        self.setWindowTitle("About " + name)


class MyStream(QtCore.QObject):
    message = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))


class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        path = sys.argv[0].split('\\')
        name = path[len(path) - 1]
        self.editor()
        self.setGeometry(200, 200, 1000, 800)
        font = QtGui.QFont("Courier", 10)
        self.setFont(font)
        self.setWindowTitle(name)
        self.create_menu()
        self.show()

    def create_menu(self):
        actionExit = QtGui.QAction("Exit", self)
        actionExit.setShortcut('Ctrl+Q')
        actionExit.setStatusTip('Exits the program')
        actionExit.triggered.connect(self.close_application)

        actionAbout = QtGui.QAction("About", self)
        actionAbout.triggered.connect(self._showAbout)

        fontChoice = QtGui.QAction("&Font", self)
        fontChoice.setShortcut('Ctrl+F')
        fontChoice.triggered.connect(self.font_choice)

        color = QtGui.QColor(0, 0, 0, 0)
        fontColor = QtGui.QAction('&Color', self)
        fontColor.setShortcut('Ctrl+C')
        fontColor.triggered.connect(self.color_picker)

        openFile = QtGui.QAction('&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.file_open)

        saveFileP = QtGui.QAction('&Save as plain text file', self)
        saveFileP.setShortcut('Ctrl+S')
        saveFileP.triggered.connect(self.file_save_plain)
        saveFileH = QtGui.QAction('&Save as HTML file', self)
        saveFileH.setShortcut('Ctrl+H')
        saveFileH.triggered.connect(self.file_save_html)

        self.aboutWindow = AboutWindow(parent=None)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFileP)
        fileMenu.addAction(saveFileH)
        fileMenu.addAction(actionExit)

        fileMenu = mainMenu.addMenu('&View')
        fileMenu.addAction(fontChoice)
        fileMenu.addAction(fontColor)

        fileMenu = mainMenu.addMenu('&Info')
        fileMenu.addAction(actionAbout)

    def on_myStream_message(self, message):
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.insertPlainText(message)

    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open messages file')
        return name

    def file_save_html(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save HTML file')
        file = open(name, 'w')
        text = self.textEdit.toHtml()
        file.write(text)
        file.close()

    def file_save_plain(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save plain text file')
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

    def font_choice(self):
        font, valid = QtGui.QFontDialog.getFont()
        if valid:
            self.textEdit.setCurrentFont(font)

    def color_picker(self):
        color = QtGui.QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def _showAbout(self):
        self.aboutWindow.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Exit", "Are you sure?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes: sys.exit()

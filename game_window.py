from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QPushButton, QWidget, QStackedWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import QTimer, Qt
from functools import partial
import random
from model import GameData
import sys


class Color(QWidget):
    """Color Palette Class"""
    def __init__(self,color,*args,**kwargs):
        super(Color,self).__init__(*args,**kwargs)
        self.setAutoFillBackground(True)

        palette=self.palette()
        palette.setColor(QPalette.Window,QColor(color))
        self.setPalette(palette)


class GameWindow(QMainWindow):
    def __init__(self, pic_paths, image_cache=None):
        """Initialize game window. Load the images (from cache if available)"""
        super(GameWindow, self).__init__()
        self.pic_paths=pic_paths
        self.image_path=""
        if image_cache is None:
            image_cache={}
        self.image_cache=image_cache
        self.stack_count=0
        self.num_images=24
        self.setGeometry(QtWidgets.QDesktopWidget().screenGeometry(-1))
        self.showMaximized()
        self.grid_layout=QGridLayout()
        self.setup_grid()
        widget=Color("#ffd966")
        widget.setLayout(self.grid_layout)
        self.setCentralWidget(widget)

    def setup_grid(self):
        """Load images to game window grid"""
        self.grid_layout.setVerticalSpacing(5)
        self.grid_layout.setHorizontalSpacing(5)
        pp = self.pic_paths.copy()
        for x in range(4):
            for y in range(6):
                stack = QStackedWidget()
                label = QLabel()
                label.setStyleSheet("background-color: lightgreen")
                path = pp.pop()
                label.setPixmap(self.get_image(path))
                label.setScaledContents(True)
                label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                button = QPushButton()
                button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                button.clicked.connect(partial(self.open_image, path))
                stack.addWidget(button)
                stack.addWidget(label)
                stack.setCurrentWidget(button)
                stack.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.grid_layout.addWidget(stack, x, y)

    def get_image(self, image_path):
        """Return image from image path"""
        if image_path in self.image_cache.keys():
            return self.image_cache[image_path]
        image = QPixmap(image_path)
        self.image_cache[image_path] = image
        return image

    def open_image(self, path):
        """Locate the image at gamewindow and display"""
        if self.stack_count == 2:
            return None
        btn = self.sender()
        stack = btn.parent()
        stack.setCurrentIndex(1)
        self.stack_count += 1
        if self.stack_count==2:
            if self.image_path==path:
                QTimer.singleShot(500, self.remove_pair)
            else:
                QTimer.singleShot(1000,self.close_images)
        else:
            self.image_path = path

    def close_images(self):
        """Make all images closed"""
        for i in range(self.grid_layout.count()):
            stk=self.grid_layout.itemAt(i).widget()
            stk.setCurrentIndex(0)
        self.stack_count=0

    def remove_pair(self):
        """Remove paif of images if both are selected."""
        for i in range(self.grid_layout.count()):
            stk=self.grid_layout.itemAt(i).widget()
            if stk.currentIndex() == 1:
                stk.removeWidget(stk.currentWidget())
                stk.removeWidget(stk.currentWidget())
                self.num_images -= 1
                if self.num_images == 0:
                    random.shuffle(self.pic_paths)
                    QTimer.singleShot(500, partial(self.initGame, self.pic_paths, self.image_cache))
        self.stack_count=0

    def keyPressEvent(self, event):
        """Switch to fullscreen and back"""
        if event.key() == Qt.Key_Escape:
            self.showMaximized()
        elif event.key() == Qt.Key_F:
            self.showFullScreen()

if __name__ == '__main__':
    data=GameData('GUEST')
    app=QtWidgets.QApplication(sys.argv)
    win = GameWindow(data.images)
    win.setWindowTitle(data.game_name)
    win.show()
    sys.exit(app.exec_())
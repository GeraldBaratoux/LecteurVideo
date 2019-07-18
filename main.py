import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_vlc import Ui_MainWindow
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pbLecture.clicked.connect(self.lectureClicked)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.wVideo)

    def lectureClicked(self):
        print("Lecture !!")
        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)
        self.mediaPlayer.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
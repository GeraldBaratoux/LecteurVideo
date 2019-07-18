import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_vlc import Ui_MainWindow
from PySide2.QtCore import QUrl, QTime
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pbLecture.clicked.connect(self.lectureClicked)
        self.ui.pbPause.clicked.connect(self.pauseClicked)
        self.ui.pbStop.clicked.connect(self.stopClicked)
        self.ui.dVolume.valueChanged.connect(self.volumeChanged)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.wVideo)

        self.mediaPlayer.durationChanged.connect(self.mediaDurationChanged)
        self.mediaPlayer.positionChanged.connect(self.mediapositionChanged)

        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)

    def lectureClicked(self):
        print("Lecture !!")
        self.mediaPlayer.play()
    def pauseClicked(self):
        print("Pause !!")
        if self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.mediaPlayer.play()
        elif self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
    def stopClicked(self):
        self.mediaPlayer.stop()
    def volumeChanged(self):
        self.mediaPlayer.setVolume(self.ui.dVolume.value())
        self.ui.lVolume.setText(str(self.ui.dVolume.value())+"%")

    def mediaDurationChanged(self):
        print("mediaLoaded")
        self.ui.lTpsCourant.setText("00:00:00")
        mediaDuration = self.mediaPlayer.duration()
        self.ui.sTpsCourant.setRange(0, mediaDuration)###############
        totalTimeMedia = QTime(0, 0, 0)
        totalTimeMedia = totalTimeMedia.addMSecs(mediaDuration)
        self.ui.lTpsTotal.setText(totalTimeMedia.toString("HH:mm:ss"))

    def mediapositionChanged(self):
        mediaPosition = self.mediaPlayer.position()
        self.ui.sTpsCourant.setValue(mediaPosition)##############
        currentTimeMedia = QTime(0, 0, 0)
        currentTimeMedia = currentTimeMedia.addMSecs(mediaPosition)
        self.ui.lTpsCourant.setText(currentTimeMedia.toString("HH:mm:ss"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
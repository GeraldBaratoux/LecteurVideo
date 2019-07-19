import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from ui_vlc import Ui_MainWindow
from PySide2.QtCore import QUrl, QTime, QFileInfo
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
        self.ui.sTpsCourant.valueChanged.connect(self.sliderPositionChanged)
        self.ui.pbAjout.clicked.connect(self.ajouterMedia2)
        self.ui.pbSuppr.clicked.connect(self.supprMedia)
        self.ui.lPlaylist.itemDoubleClicked.connect(self.mediaSelected2)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.wVideo)

        self.mediaPlayer.durationChanged.connect(self.mediaDurationChanged)
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)

        self.ui.pbSuivant.clicked.connect(self.suivantClicked)
        self.ui.pbPrecedent.clicked.connect(self.precedentClicked)

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

    def mediaPositionChanged(self):
        self.ui.sTpsCourant.valueChanged.disconnect(self.sliderPositionChanged)
        mediaPosition = self.mediaPlayer.position()
        self.ui.sTpsCourant.setValue(mediaPosition)##############
        currentTimeMedia = QTime(0, 0, 0)
        currentTimeMedia = currentTimeMedia.addMSecs(mediaPosition)
        self.ui.lTpsCourant.setText(currentTimeMedia.toString("HH:mm:ss"))
        self.ui.sTpsCourant.valueChanged.connect(self.sliderPositionChanged)

    def sliderPositionChanged(self):
        self.mediaPlayer.positionChanged.disconnect(self.mediaPositionChanged)
        self.mediaPlayer.setPosition(self.ui.sTpsCourant.value())
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)

    def ajouterMedia(self):
        nomMedia = QFileDialog.getOpenFileName(self,"Choix Film", "c:/", "Movie Files (*.avi *.mp4)")
        item = QListWidgetItem(nomMedia[0])
        self.ui.lPlaylist.addItem(item)

    def ajouterMedia2(self):
        nomMedia = QFileDialog.getOpenFileName(self, "Choix Film", "c:/", "Movie Files (*.avi *.mp4)")

        if nomMedia[0] == "": #si aucun fichier selectionné
            return

        fInfo = QFileInfo(nomMedia[0])
        fShortName = fInfo.baseName()
        item = QListWidgetItem(fShortName)
        item.setToolTip(nomMedia[0])
        self.ui.lPlaylist.addItem(item)

    def supprMedia(self):
        rowItem = self.ui.lPlaylist.currentRow()
        if rowItem != -1:
            self.ui.lPlaylist.takeItem(rowItem)

    def mediaSelected(self):
        currentItem = self.ui.lPlaylist.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.text()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

    def mediaSelected2(self):
        currentItem = self.ui.lPlaylist.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.toolTip()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

    def suivantClicked(self):
        currentItemRow = self.ui.lPlaylist.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.lPlaylist.count()
        self.ui.lPlaylist.setCurrentRow((currentItemRow+1)%totalItems)
        self.mediaSelected2()

    def precedentClicked(self):
        currentItemRow = self.ui.lPlaylist.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.lPlaylist.count()
        self.ui.lPlaylist.setCurrentRow((currentItemRow-1)%totalItems)
        self.mediaSelected2()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
import sys
import os
import numpy as np

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QEvent
from PySide6.QtGui import QPixmap, QImage

from PIL import Image

from logic.compressor import compress

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Variabili
        self.F = 1
        self.d = 0
        self.FMax = 0
        self.dMax = 0
        self.img_caricata = None
        self.larghezza = 0
        self.altezza = 0

        # Trova il percorso assoluto del file form.ui nella cartella gui
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "gui", "form.ui")

        # Carica il file UI in modo dinamico
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if ui_file.open(QFile.ReadOnly):
            self.ui = loader.load(ui_file, self)
            ui_file.close()

            # Modifiche iniziali
            self.setCentralWidget(self.ui.centralWidget())
            self.showMaximized()

            self.setWindowTitle("Compressore JPEG")

            # Creo le scene per gestire le immagini dentro i riquadri
            self.scena_orig = QGraphicsScene(self)
            self.scena_compr = QGraphicsScene(self)
            self.ui.imgOrigView.setScene(self.scena_orig)
            self.ui.imgComprView.setScene(self.scena_compr)

            # Abilito zoom
            self.ui.imgOrigView.installEventFilter(self)
            self.ui.imgComprView.installEventFilter(self)

            self.ui.imgOrigView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.ui.imgOrigView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
            self.ui.imgComprView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.ui.imgComprView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

            # Abilito panning (con puntatore classico)
            self.ui.imgOrigView.setDragMode(QGraphicsView.ScrollHandDrag)
            self.ui.imgComprView.setDragMode(QGraphicsView.ScrollHandDrag)
            self.ui.imgOrigView.viewport().setCursor(Qt.ArrowCursor)
            self.ui.imgComprView.viewport().setCursor(Qt.ArrowCursor)

            # Collego UI con Segnali e Slot
            self.ui.fileSysPushButton.clicked.connect(self.filesystem_click)
            self.ui.calcolaImgButton.clicked.connect(self.calcolaImg_click)
            self.ui.fSpinBox.valueChanged.connect(self.spinBoxF)
            self.ui.dSpinBox.valueChanged.connect(self.spinBoxD)

        else:
            print(f"Impossibile caricare il file UI da: {ui_path}")

    def filesystem_click(self):
        # Scelta nel filesystem
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona un file",
            "../data/",
            "Immagine bitmap (*.bmp);;"
        )
        # Controllo se l'utente ha scelto qualcosa
        if file_path:
            try:
                # Carico img
                self.img_caricata = Image.open(file_path).convert('L')

                self.larghezza, self.altezza = self.img_caricata.size
                self.dMax = 2 * self.F - 2
                self.FMax = min(self.larghezza, self.altezza)

                # Aggiorno limiti spin box
                self.ui.fSpinBox.setEnabled(True);
                self.ui.fSpinBox.setMaximum(self.FMax)

                self.ui.dSpinBox.setEnabled(True);
                self.ui.dSpinBox.setMaximum(self.dMax)

                # Messaggio sul bottone (log)
                self.ui.fileSysPushButton.setStyleSheet("font-style: italic;")
                self.ui.fileSysPushButton.setText(f"Immagine: {file_path}")

                self.ui.fLabel.setText(f"Inserisci la grandezza dei blocchi F (Max {self.FMax})")
                self.ui.dLabel.setText(f"Inserisci la soglia di taglio d (Max {self.dMax})")
                self.ui.calcolaImgButton.setEnabled(True);

                # print("Nuova immagine selezionata")

            except Exception as e:
                self.ui.fileSysPushButton.setText(f"Errore caricamento: {e}")
                self.immagine_path = None
                self.img_caricata = None

    # Metodo più efficiente rispetto alla conversione con BytesIO
    def numpy_to_pixmap(self, array_2d):
        array_uint8 = np.ascontiguousarray(array_2d.astype(np.uint8))
        altezza, larghezza = array_uint8.shape

        # Creo QImage che punta direttamente ai dati dell'array in memoria
        q_img = QImage(array_uint8.data, larghezza, altezza, larghezza, QImage.Format_Grayscale8)

        return QPixmap.fromImage(q_img)

    def eventFilter(self, target_widget, event):
        if event.type() == QEvent.Type.Wheel and target_widget in (self.ui.imgOrigView, self.ui.imgComprView):
            if event.modifiers() == Qt.ControlModifier:
                fattore_zoom = 1.15

                # Calcoliamo il livello di zoom attuale per evitare eccessi
                # m11 rappresenta la scala sull'asse X
                scala_attuale = target_widget.transform().m11()

                if event.angleDelta().y() > 0:
                    # Zoom In (limite massimo a 30x)
                    if scala_attuale < 30.0:
                        target_widget.scale(fattore_zoom, fattore_zoom)
                else:
                    # Zoom Out (limite minimo allo 0.1x)
                    if scala_attuale > 0.1:
                        target_widget.scale(1.0 / fattore_zoom, 1.0 / fattore_zoom)

                # Ritorna True per dire a Qt: "Ho gestito io la rotella, NON muovere le barre laterali!"
                return True

            # Forzo il cursore a rimanere puntatore
            if event.type() in (QEvent.Type.MouseMove, QEvent.Type.MouseButtonRelease, QEvent.Type.Enter):
                if target_widget.viewport().cursor().shape() != Qt.ArrowCursor:
                    target_widget.viewport().setCursor(Qt.ArrowCursor)

        return super().eventFilter(target_widget, event)

    def calcolaImg_click(self):
        # Scrivo label sopra le img
        self.ui.textOrigLabel.setStyleSheet("font-weight: bold;")
        self.ui.textOrigLabel.setText("Immagine originale")
        self.ui.textOrigLabel.setAlignment(Qt.AlignCenter)

        self.ui.textComprLabel.setStyleSheet("font-weight: bold;")
        self.ui.textComprLabel.setText(f"Immagine compressa: F = {self.F}, d = {self.d}")
        self.ui.textComprLabel.setAlignment(Qt.AlignCenter)

        # Calcolo compressione
        original_img_array = np.array(self.img_caricata)
        compressed_img_array, h_new, w_new = compress(original_img_array, self.F, self.d)

        # Mostro le img nelle label (le devo riconvertirle)
        pixmap_orig = self.numpy_to_pixmap(original_img_array)
        pixmap_compr = self.numpy_to_pixmap(compressed_img_array)

        # Pulisco scena dalle vecchie img
        self.scena_orig.clear()
        self.scena_compr.clear()

        # Aggiungiamo le nuove foto a dimensione reale
        self.scena_orig.addPixmap(pixmap_orig)
        self.scena_compr.addPixmap(pixmap_compr)

        # Resetto le inquadrature iniziali per fare in modo che l'immagine
        # appena caricata entri tutta nel riquadro senza zoom iniziale
        self.ui.imgOrigView.resetTransform()
        self.ui.imgComprView.resetTransform()
        self.ui.imgOrigView.fitInView(self.scena_orig.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.ui.imgComprView.fitInView(self.scena_compr.itemsBoundingRect(), Qt.KeepAspectRatio)

        # print("Immagine compressa calcolata e stampata")

    def spinBoxF(self, nuovo_F):
        # Modifico valore di F e aggiorno il max di d
        self.F = nuovo_F
        self.dMax = 2 * self.F - 2
        self.ui.dLabel.setText(f"Inserisci la soglia di taglio d (Max {self.dMax})")
        self.ui.dSpinBox.setMaximum(self.dMax)
        # print("Settato nuovo F")

    def spinBoxD(self, nuovo_d):
        # Modifico solamente valore di d
        self.d = nuovo_d
        # print("Settato nuovo d")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
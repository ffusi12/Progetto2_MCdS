import sys
import os
import numpy as np
from io import BytesIO

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QPixmap

from PIL import Image

from logic.compressor import compress

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Forward decl
        self.F = 1
        self.d = 0
        self.dMax = 0
        self.img_caricata = None

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
            self.stile_riquadro = """
                QLabel {
                    border: 2px solid #bdc3c7;      /* Bordo grigio chiaro */
                    border-radius: 6px;             /* Angoli leggermente arrotondati */
                    background-color: #f8f9fa;      /* Sfondo grigio chiarissimo */
                    padding: 4px;                   /* Spazio interno tra bordo e immagine */
                }
            """

            self.setWindowTitle("Compressore JPEG")

            # Collego UI con Segnali e Slot
            # 2 Bottoni
            self.ui.fileSysPushButton.clicked.connect(self.filesystem_click)
            self.ui.calcolaImgButton.clicked.connect(self.calcolaImg_click)

            # 2 Spin box per valori
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

                larghezza, altezza = self.img_caricata.size

                # Aggiorno limiti spin box
                self.ui.fSpinBox.setEnabled(True);
                self.ui.fSpinBox.setMinimum(1)
                self.ui.fSpinBox.setMaximum(larghezza)

                self.ui.dSpinBox.setEnabled(True);
                self.ui.dSpinBox.setMinimum(0)
                self.ui.dSpinBox.setMaximum(altezza)

                # Messaggio sul bottone (log)
                self.ui.fileSysPushButton.setStyleSheet("font-style: italic;")
                self.ui.fileSysPushButton.setText(f"Immagine: {file_path}")

                self.dMax = 2 * self.F - 2
                self.ui.fLabel.setText(f"Inserisci la grandezza dei blocchi F (Max {larghezza})")
                self.ui.dLabel.setText(f"Inserisci la soglia di taglio d (Max {self.dMax})")
                self.ui.calcolaImgButton.setEnabled(True);

                # print("Nuova immagine selezionata")

            except Exception as e:
                self.ui.fileSysPushButton.setText(f"Errore caricamento: {e}")
                self.immagine_path = None
                self.img_caricata = None

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

        # Mostro le img nelle label (le devo convertire in QPixMap)
        # Img originale
        buffer_orig = BytesIO()
        self.img_caricata.save(buffer_orig, format="BMP")
        pixmap_orig = QPixmap()
        pixmap_orig.loadFromData(buffer_orig.getvalue())
        self.ui.imgOrigLabel.setStyleSheet(self.stile_riquadro)
        self.ui.imgOrigLabel.setPixmap(pixmap_orig)
        self.ui.imgOrigLabel.setAlignment(Qt.AlignCenter)

        # Img Compressa
        compressed_img = Image.fromarray(compressed_img_array.astype(np.uint8))
        buffer_compr = BytesIO()
        compressed_img.save(buffer_compr, format="BMP")
        pixmap_compr = QPixmap()
        pixmap_compr.loadFromData(buffer_compr.getvalue())
        self.ui.imgComprLabel.setStyleSheet(self.stile_riquadro)
        self.ui.imgComprLabel.setPixmap(pixmap_compr)
        self.ui.imgComprLabel.setAlignment(Qt.AlignCenter)

        # print("Immagine compressa calcolata e stampata")

    def spinBoxF(self, nuovo_F):
        # Modifico valore di F e aggiorno il max di d
        self.F = nuovo_F
        self.dMax = 2 * self.F - 2
        self.ui.dLabel.setText(f"Inserisci la soglia di taglio d (Max {self.dMax})")
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
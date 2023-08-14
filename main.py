import sys
import qrcode
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageQt
import cv2

def create_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def read_qr_code_from_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    qr_code_detector = cv2.QRCodeDetector()
    retval, decoded_info, points, _ = qr_code_detector.detectAndDecodeMulti(image)
    if retval:
        return decoded_info[0]  # Extract the first element (text) from the tuple
    return None

class QRCodeGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def create_qr_code(self):
        data = self.text_edit.toPlainText().strip()
        if data:
            try:
                img = create_qr_code(data)
                qimage = ImageQt.ImageQt(img)  # Convert PIL.Image.Image to QImage
                pixmap = QPixmap.fromImage(qimage)
                self.result_label.setPixmap(pixmap)
                self.result_label.show()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Erstellen des QR-Codes: {e}")
        else:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie Text ein, um einen QR-Code zu erstellen.")

    def save_qr_code(self):
        data = self.text_edit.toPlainText().strip()
        if data:
            try:
                img = create_qr_code(data)
                qimage = ImageQt.ImageQt(img)  # Convert PIL.Image.Image to QImage
                pixmap = QPixmap.fromImage(qimage)
                file_path, _ = QFileDialog.getSaveFileName(self, "QR Code speichern", "", "PNG-Datei (*.png);;Alle Dateien (*)")
                if file_path:
                    pixmap.save(file_path, "PNG")
                    QMessageBox.information(self, "Erfolg", "QR-Code wurde erfolgreich gespeichert.")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Erstellen des QR-Codes: {e}")
        else:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie Text ein, um einen QR-Code zu erstellen.")

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Bilddateien (*.png *.jpg *.jpeg);;Alle Dateien (*)")
        if file_path:
            try:
                data = read_qr_code_from_image(file_path)
                if data:
                    self.text_edit.setPlainText(data)
                else:
                    QMessageBox.warning(self, "Warnung", "Kein QR-Code in der ausgewählten Datei gefunden.")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Lesen der Datei: {e}")

    def initUI(self):
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        generate_button = QPushButton("QR Code erstellen", self)
        generate_button.clicked.connect(self.create_qr_code)
        layout.addWidget(generate_button)

        save_button = QPushButton("QR Code speichern", self)
        save_button.clicked.connect(self.save_qr_code)
        layout.addWidget(save_button)

        browse_button = QPushButton("Durchsuchen", self)
        browse_button.clicked.connect(self.browse_file)
        layout.addWidget(browse_button)

        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGeneratorApp()
    window.show()
    sys.exit(app.exec_())

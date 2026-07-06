from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Astra AI")

        self.resize(1400, 900)

        self.build_ui()

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("⚡ Astra AI")

        title.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:#10B981;
        """)

        subtitle = QLabel(
            "Desktop AI Assistant\nVersion 0.2.0"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(title)

        layout.addWidget(subtitle)
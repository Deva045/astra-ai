from pathlib import Path


def load_theme(app):

    qss = (
        Path(__file__)
        .parent
        .joinpath("styles", "dark.qss")
    )

    if qss.exists():

        app.setStyleSheet(qss.read_text())
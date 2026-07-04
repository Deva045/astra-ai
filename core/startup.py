import time

from core.logger import app_logger


class Startup:

    def __init__(self):

        self.steps = [
            "Loading Configuration",
            "Loading Logger",
            "Loading Database",
            "Loading Memory",
            "Loading User Interface",
        ]

    def run(self):

        for step in self.steps:

            app_logger.info(step)

            time.sleep(0.4)

        app_logger.success("Astra AI Ready")
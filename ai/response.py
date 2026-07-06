from dataclasses import dataclass


@dataclass
class Response:

    success: bool

    message: str
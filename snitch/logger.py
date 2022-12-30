from dataclasses import dataclass


@dataclass
class LogItem:
    has_err: bool
    run_time: float
    message: str
    name: str = ""

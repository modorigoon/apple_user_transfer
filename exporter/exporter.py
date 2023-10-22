from abc import ABC, abstractmethod


class Exporter(ABC):

    def __init__(self, file_name: str):
        self.file_name = file_name

    @abstractmethod
    def export(self, results: list):
        pass

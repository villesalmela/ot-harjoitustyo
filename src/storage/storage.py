from abc import ABC, abstractmethod


class Storage(ABC):
    """Abstract class for storage backend.
    """

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def save(self, data, name) -> None:
        pass

    @abstractmethod
    def load(self, name) -> None:
        pass

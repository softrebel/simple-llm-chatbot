from abc import ABC, abstractmethod


class SearchError(Exception): ...


class SearchEngine(ABC):
    @abstractmethod
    def search(self, query: str) -> list[dict]:
        raise NotImplementedError

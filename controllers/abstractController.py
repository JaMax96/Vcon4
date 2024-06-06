from abc import ABC, abstractmethod

class AbstractController(ABC):

    @abstractmethod
    def getMenuItem(self):
        pass

    @abstractmethod
    def getMove(self):
        pass
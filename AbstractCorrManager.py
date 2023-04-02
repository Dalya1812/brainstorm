from abc import ABC, abstractmethod

class AbstractCorrManager(ABC):

    @abstractmethod
    def get_corr(self):
        pass
from abc import ABC, abstractmethod


class MenuElement(ABC):
    @abstractmethod
    def blit(self, surface):
        pass

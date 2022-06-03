from abc import ABC, abstractmethod


class MenuElement(ABC):
    @abstractmethod
    def blit(self, surface):
        pass


class AnimatedMenuElement(MenuElement):
    @abstractmethod
    def animate(self):
        pass

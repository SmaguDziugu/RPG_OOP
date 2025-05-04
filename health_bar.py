import os

os.system("")

class HealthBar:
    _symbol_remaining: str = "▉"
    _symbol_lost: str = "_"
    _barrier: str = "|"
    _colors: dict = {"red": "\033[91m",
                    "green": "\033[92m",
                    "default": "\033[0m"}
    def __init__(self, entity, length: int = 20, is_colored: bool = True, color: str = "") -> None:
        self._entity = entity
        self._length = length
        self._max_value = entity.max_health
        self._current_value = entity.health
        self._is_colored = is_colored
        self._color = self._colors.get(color) or self._colors["default"]

    @property
    def entity(self):
        return self._entity
        
    @property
    def length(self):
        return self._length
        
    @property
    def is_colored(self):
        return self._is_colored
        
    @property
    def color(self):
        return self._color

    def update(self) -> None:
        self._current_value = self._entity.health

    def draw(self) -> None:
        remaining_bars = round(self._current_value / self._max_value * self._length)
        lost_bars = self._length - remaining_bars
        current_health = round(self._entity.health, 1)
        max_health = round(self._entity.max_health, 1)
        print(f"{self._entity.name}'s HEALTH: {current_health}/{max_health}")
        print(f"{self._barrier}"
              f"{self._color if self._is_colored else ''}"
              f"{remaining_bars * self._symbol_remaining}"
              f"{lost_bars * self._symbol_lost}"
              f"{self._colors['default'] if self._is_colored else ''}"
              f"{self._barrier}")
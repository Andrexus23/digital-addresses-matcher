"""Базовый класс инициализатора моделей."""
from os import getpid
from typing import Optional, Any


class ModelInitializer:
    def __init__(self) -> None:
        """Конструктор."""
        self._pid: Optional[int] = None
        self._model: Any = None

    def __call__(self) -> Any:
        """Вызов модели."""
        pid = getpid()
        if pid != self._pid:
            self._model = self._inner_get_model()
            self._pid = pid
        return self._model
    
    def _inner_get_model(self) -> Any:
        """Метод для инициализации модели (Предполагается переопределять)."""

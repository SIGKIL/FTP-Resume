from abc import (ABC, abstractmethod)
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .persist_model import PersistModel


class ABCPersistor(ABC):

    @abstractmethod
    def get_model(self, persist_model: 'PersistModel') -> Optional['PersistModel']:
        pass

    @abstractmethod
    def save_model(self, persist_model: 'PersistModel'):
        pass

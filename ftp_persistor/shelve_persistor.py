from typing import (Optional, TYPE_CHECKING, Tuple)
from .abc_persistor import ABCPersistor
from utils import cast_path
from shelve import (Shelf, open as create_shelve)
from hashlib import md5
if TYPE_CHECKING:
    from ftp_resume_types import PATH_TYPE
    from .persist_model import PersistModel


class ShelvePersistor(ABCPersistor):
    def __init__(self, shelve_path: 'PATH_TYPE'):
        self._shelve_path = cast_path(shelve_path)
        self._shelve: Optional[Shelf] = None
        self._initialize_shelve()

    @classmethod
    def _get_storage_key(cls, persist_model: 'PersistModel') -> str:
        data = f"{persist_model.file!s}\n{persist_model.storage_path!s}"
        return md5(data.encode()).hexdigest()

    def _initialize_shelve(self):
        self._shelve = create_shelve(str(self._shelve_path))

    def get_model(self, persist_model: 'PersistModel') -> Optional['PersistModel']:
        storage_key = self._get_storage_key(persist_model=persist_model)
        return self._shelve.get(storage_key, None)

    def save_model(self, persist_model: 'PersistModel'):
        storage_key = self._get_storage_key(persist_model=persist_model)
        self._shelve[storage_key] = persist_model
        self._shelve.sync()

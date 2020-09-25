from typing import (TYPE_CHECKING, Type, Tuple)
from abc import (ABC, abstractmethod)
if TYPE_CHECKING:
    from ftp_persistor import PersistModel
    from pathlib import Path
    from ftp_resume_types import PATH_TYPE
    from ftp_persistor import ABCPersistor


class ABCResumeController(ABC):

    @classmethod
    @abstractmethod
    def _get_persist_model_class(cls) -> Type['PersistModel']:
        pass

    @abstractmethod
    def _new_part_file(self, file: 'Path', storage_path: 'Path', part_index: int) -> 'Path':
        pass

    def __init__(self, ftp_persistor: 'ABCPersistor'):
        self._ftp_persistor = ftp_persistor
        self._persist_model_class = self._get_persist_model_class()

    def _save_model(self, persist_model: 'PersistModel'):
        self._ftp_persistor.save_model(persist_model=persist_model)

    def _create_model(self, file: 'PATH_TYPE', storage_path: 'PATH_TYPE') -> 'PersistModel':
        return self._persist_model_class(file=file, storage_path=storage_path)

    def get_model(self, file: 'PATH_TYPE', storage_path: 'PATH_TYPE') -> 'PersistModel':
        model = self._create_model(file=file, storage_path=storage_path)
        stored_model = self._ftp_persistor.get_model(persist_model=model)
        return stored_model or model

    def resume_info(self, persist_model: 'PersistModel') -> Tuple['Path', int]:
        resume_size = 0
        for file_part in persist_model.parts:
            resume_size += file_part.stat().st_size
        part_index = len(persist_model.parts)
        part_file = self._new_part_file(persist_model.file, persist_model.storage_path, part_index)
        persist_model.parts.append(part_file)
        self._save_model(persist_model=persist_model)
        return part_file, resume_size

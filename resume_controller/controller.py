from typing import (Type, TYPE_CHECKING)
from .abc_controller import ABCResumeController
from ftp_persistor import PersistModel
if TYPE_CHECKING:
    from pathlib import Path


class ResumeController(ABCResumeController):

    def __init__(self, *args, **kwargs):
        super(ResumeController, self).__init__(*args, **kwargs)
        self._file_name_part_pattern = "{file_name}_[{part_index:03d}]"

    @classmethod
    def _get_persist_model_class(cls) -> Type[PersistModel]:
        return PersistModel

    def _new_part_file(self, file: 'Path', storage_path: 'Path', part_index: int) -> 'Path':
        file_name = self._file_name_part_pattern.format(
            file_name=file.stem, part_index=part_index
        )
        file_name = f"{file_name}{file.suffix}"
        parted_file = storage_path.joinpath(file_name)
        return parted_file

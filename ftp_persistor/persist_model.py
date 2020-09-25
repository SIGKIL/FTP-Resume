from ftp_resume_types import (PATH_TYPE, FTP_RESUME_PART)
from typing import Optional, List, TYPE_CHECKING
from utils import cast_path
if TYPE_CHECKING:
    from pathlib import Path


class PersistModel:

    def __init__(self,
                 file: PATH_TYPE, storage_path: PATH_TYPE,
                 parts: Optional[FTP_RESUME_PART] = None,
                 ):
        self.file = cast_path(file)
        self.storage_path = cast_path(storage_path)
        self.parts: List['Path'] = list()
        if self.parts:
            self.parts = list(parts)



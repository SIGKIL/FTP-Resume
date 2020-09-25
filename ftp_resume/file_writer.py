from typing import (TYPE_CHECKING, BinaryIO, Optional, Callable)
if TYPE_CHECKING:
    from pathlib import Path
    from ftp_persistor import PersistModel


class FTPFileWriter:
    def __init__(self, persist_model: 'PersistModel', parted_file: 'Path'):
        self._persist_model = persist_model
        self._parted_file = parted_file
        self._parted_file_buffer: Optional[BinaryIO] = None

    def __enter__(self) -> Callable:
        self._parted_file_buffer = self._parted_file.open("wb")
        return self.__call__

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._parted_file_buffer is not None and self._parted_file_buffer.closed is False:
            self._parted_file_buffer.close()

    def __call__(self, data: bytes):
        self._parted_file_buffer.write(data)
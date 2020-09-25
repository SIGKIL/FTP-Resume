from typing import (TYPE_CHECKING, Type)
import ftplib
if TYPE_CHECKING:
    from .file_writer import FTPFileWriter
    from ftp_resume_types import PATH_TYPE
    from resume_controller import ABCResumeController


class FTPResume:
    def __init__(self,
                 resume_controller: 'ABCResumeController',
                 file_writer: Type['FTPFileWriter'],
                 ftp_client: 'ftplib.FTP'
                 ):
        self._resume_controller = resume_controller
        self._file_writer = file_writer
        self._ftp_client = ftp_client

    def __call__(self, file: 'PATH_TYPE', storage_path: 'PATH_TYPE'):
        resume_model = self._resume_controller.get_model(
            file=file, storage_path=storage_path
        )
        parted_file, resume_size = self._resume_controller.resume_info(persist_model=resume_model)
        rest = resume_size or None

        with self._file_writer(persist_model=resume_model, parted_file=parted_file) as fp:
            self._ftp_client.retrbinary(f"RETR {file.name}", fp, rest=rest)
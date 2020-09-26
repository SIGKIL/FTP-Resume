from typing import (Optional, TYPE_CHECKING)
from urllib.parse import urlparse
from ftp_resume import (FTPResume, FTPFileWriter)
from ftp_persistor import ShelvePersistor
from resume_controller import ResumeController
import pathlib
import argparse
import ftplib
if TYPE_CHECKING:
    from ftp_persistor import ABCPersistor
    from resume_controller import ABCResumeController


class Args:

    def __init__(self):
        self._args = argparse.ArgumentParser(
            prog="FTPResume",
            description="Testing FTP Resume"

        )
        self._add_args()

    def _add_args(self):
        self._args.add_argument(
            "-fs", "--ftp_server", dest="ftp_server", required=True, type=str, help="bind address, [IP]:[PORT]"
        )

        self._args.add_argument(
            "-u", "--user", dest="user", required=True, type=str, help="FTP account name"
        )
        self._args.add_argument(
            "-p", "--password", dest="password", required=True, type=str, help="FTP account password"
        )
        self._args.add_argument(
            "-f", "--file", dest="file", required=True, type=str, help="FTP file will download"
        )
        self._args.add_argument(
            "-sp", "--storage_path", required=False, dest="storage_path", type=str, help="Downloaded file path"
        )

    def parameters(self) -> argparse.Namespace:
        return self._args.parse_args()


class FTPDownloader:
    def __init__(self):
        self._args = Args()
        self._parameters = self._args.parameters()
        self._ftp: Optional['ftplib.FTP'] = None
        self._storage_path: Optional['pathlib.Path'] = None
        self._persistor: Optional['ABCPersistor'] = None
        self._resume_controller: Optional['ABCResumeController'] = None
        self._ftp_resume: Optional['FTPResume'] = None

        self._init_ftp()
        self._init_storage_path()
        self._init_persistor()
        self._init_controller()
        self._init_resume()

    def _init_ftp(self):
        self._ftp = ftplib.FTP()
        ftp_server = self._parameters.ftp_server
        url = urlparse(ftp_server)
        if url.scheme is None:
            raise ValueError("bad scheme, use ftp://")

        self._ftp.connect(host=url.hostname, port=url.port or 21)
        self._ftp.login(user=self._parameters.user, passwd=self._parameters.password)

    def _init_storage_path(self):
        storage_path_param = self._parameters.storage_path
        self._storage_path = pathlib.Path(storage_path_param)
        if not self._storage_path.exists():
            self._storage_path.mkdir(parents=True)

    def _init_persistor(self):
        shelve_path = self._storage_path.joinpath("persistor.bin")
        self._persistor = ShelvePersistor(shelve_path=shelve_path)

    def _init_controller(self):
        self._resume_controller = ResumeController(
            ftp_persistor=self._persistor
        )

    def _init_resume(self):
        self._ftp_resume = FTPResume(
            resume_controller=self._resume_controller,
            file_writer=FTPFileWriter,
            ftp_client=self._ftp
        )

    def download(self):
        file = pathlib.Path(self._parameters.file)
        storage_path = pathlib.Path(self._parameters.storage_path)
        if storage_path.is_file():
            pass
        if not storage_path.exists():
            storage_path.mkdir(parents=True)
        self._ftp_resume(file=file, storage_path=storage_path)


if __name__ == "__main__":
    FTPDownloader().download()

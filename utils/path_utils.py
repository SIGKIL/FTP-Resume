from typing import TYPE_CHECKING
from pathlib import Path
if TYPE_CHECKING:
    from ftp_resume_types import PATH_TYPE


def cast_path(input_file: 'PATH_TYPE') -> 'Path':
    if isinstance(input_file, str):
        return Path(input_file)
    if isinstance(input_file, Path):
        return input_file
    raise ValueError(f"Cannot cast {type(input_file)} to Path Object")
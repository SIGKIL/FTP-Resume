"""
Setup wrote Base on https://realpython.com/pypi-publish-python-package/ tutorial
"""
import pathlib
from setuptools import setup

# The directory containing this file
BASE_DIR = pathlib.Path(__file__).parent

# The text of the README file
README = BASE_DIR.joinpath("README.md").read_text()

# This call to setup() does all the work
setup(
    name="ftp-resume",
    version="1.0.0",
    description="Resumable FTP download",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SIGKIL/FTP-Resume/",
    author="SIGKILL",
    author_email="",
    license="MIT",
    keywords = ['FTP', 'DOWNLOAD', 'RESUME', "RESUMABLE"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    scripts=['ftp_resume_types.py'],
    packages=["ftp_resume", "ftp_persistor", "resume_controller", "utils",],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ftp-resume=ftp_resume.__main__:main",
        ]
    },
)
# coding: utf-8

# Generic libs.
import logging
import os
import re

# Logger.
logger = logging.getLogger(__name__)


def mv_file(file, dest):
    """Move file to dest."""
    os.makedirs(dest, exist_ok=True)
    os.rename(file, os.path.join(dest, os.path.basename(file)))
    logger.info(f"Moved {file} to {dest}")


def list_files(path, pattern=None):
    """Return list of files in path."""
    if not isinstance(path, str):
        raise ValueError('path must be as string (str).')
    
    # List files.
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except Exception as e:
        logger.error(e)
        files = []

    # Filter on certain file name pattern.
    if pattern:
        regex = re.compile(pattern)
        files = list(filter(regex.match, files))

    # Make list of absolute paths.
    files = [os.path.join(path, f) for f in files]
    return files

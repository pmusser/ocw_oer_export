"""
Module for deleting a file.
"""

import os


def delete_file(file_path):
    """Delete a file if it exists"""
    if os.path.exists(file_path):
        os.remove(file_path)

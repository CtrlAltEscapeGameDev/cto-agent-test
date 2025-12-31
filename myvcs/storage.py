"""Content-addressed storage for myvcs."""

import hashlib
import os
from myvcs import utils


OBJECTS_DIR = os.path.join(utils.MYVCS_DIR, "objects")


def compute_hash(content):
    """
    Compute SHA-256 hash of content.
    Returns hex string for use as filename.
    """
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def store_object(content):
    """
    Store content in objects directory.
    Returns the hash of the stored content.
    """
    content_hash = compute_hash(content)
    object_path = os.path.join(OBJECTS_DIR, content_hash)
    
    # Don't store if already exists (deduplication)
    if not utils.file_exists(object_path):
        if isinstance(content, str):
            content = content.encode("utf-8")
        utils.write_file_binary(object_path, content)
    
    return content_hash


def retrieve_object(content_hash):
    """
    Retrieve content from objects directory by hash.
    Returns content as bytes.
    """
    object_path = os.path.join(OBJECTS_DIR, content_hash)
    if not utils.file_exists(object_path):
        raise FileNotFoundError(f"Object {content_hash} not found")
    return utils.read_file_binary(object_path)


def object_exists(content_hash):
    """Check if object exists in storage."""
    object_path = os.path.join(OBJECTS_DIR, content_hash)
    return utils.file_exists(object_path)

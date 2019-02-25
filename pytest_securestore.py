# -*- coding: utf-8 -*-

from io import BytesIO
from os import getenv

import pytest
from pyAesCrypt import decryptStream as decrypt
from yaml import load as load_yaml


__all__ = ["store"]


def pytest_addoption(parser):
    """Add an option to pass the decryption password and an encrypted store."""
    group = parser.getgroup("securestore", "Secure storage")
    group.addoption(
        "--secure-store-password",
        action="store",
        dest="secure_store_password",
        default=getenv("SECURE_STORE_PASSWORD", None),
        help="Set the secure storage decryption password."
    )
    group.addoption(
        "--secure-store-filename",
        action="store",
        dest="secure_store_filename",
        default=getenv("SECURE_STORE_FILE", None),
        help="Set the secure storage path and filename."
    )

    parser.addini(
        name="secure_store_password",
        help="Set the secure storage decryption password.",
        default=getenv("SECURE_STORE_PASSWORD", None)
    )
    parser.addini(
        name="secure_store_filename",
        help="Set the secure storage path and filename.",
        default=getenv("SECURE_STORE_FILE", None)
    )


@pytest.fixture(scope="module")
def store(request):
    """Decrypt a YAML file and return a value dictionary."""
    password = request.config.option.secure_store_password
    file = request.config.option.secure_store_filename
    buffer_size = 64 * 1024  # 64K decryption buffer

    # Read in the encrypted, binary file
    with open(file, "rb") as store_in:
        lines = b''
        for line in store_in.readlines():
            lines = lines + line
        encrypted = BytesIO(lines)

    # Decrypt the stream
    stream_length = len(encrypted.getvalue())
    decrypted = BytesIO()
    encrypted.seek(0)
    decrypt(encrypted, decrypted, password, buffer_size, stream_length)
    return load_yaml(decrypted.getvalue().decode("utf-8"))

# -*- coding: utf-8 -*-

from io import BytesIO
from os import getenv

import pytest
from pyAesCrypt import decryptStream as decrypt
from yaml import safe_load as load_yaml


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
        default=getenv("SECURE_STORE_FILENAME", None),
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
        default=getenv("SECURE_STORE_FILENAME", None)
    )


class Secret:
    def __init__(self, value):
        self.set_value(value)

    def __repr__(self):
        return "Secret(********)"

    def __str__(self):
        return "********"

    def __eq__(self, other_value):
        if not isinstance(other_value, str):
            return NotImplemented
        return self._value == other_value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def del_value(self):
        del self._value

    value = property(get_value, set_value, del_value)


def replace_item(obj, key):
    """Replace a specific key with a Secret value, recursively."""
    for k, value in obj.items():
        if isinstance(value, dict):
            obj[k] = replace_item(value, key)
    if key in obj:
        obj[key] = Secret(obj[key])
    return obj


@pytest.fixture(scope="module")
def store(request):
    """Decrypt a YAML file and return a value dictionary."""
    file = request.config.option.secure_store_filename
    if not file:
        file = request.config.getini('secure_store_filename')
    password = request.config.option.secure_store_password
    if not password:
        password = request.config.getini('secure_store_password')
    buffer_size = 64 * 1024  # 64K decryption buffer

    # Read in the encrypted, binary file
    with open(str(file), "rb") as store_in:
        lines = b''
        for line in store_in.readlines():
            lines = lines + line
        encrypted = BytesIO(lines)

    # Decrypt the stream
    stream_length = len(encrypted.getvalue())
    decrypted = BytesIO()
    encrypted.seek(0)
    decrypt(encrypted, decrypted, password, buffer_size, stream_length)
    temp_obj = load_yaml(decrypted.getvalue().decode("utf-8"))
    return replace_item(temp_obj, 'password')

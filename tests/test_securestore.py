# -*- coding: utf-8 -*-

from io import BytesIO
from pyAesCrypt import encryptStream
from yaml import load as load_yaml

BUFFER_SIZE = 64 * 1024  # suggested 64K for the encryption buffer
PLUGIN_NAME = "securestore"
GENERIC_PASSWORD = "BAD_password!"
YML_FILE = """---
# a comment
general_user:
    username: {username}
    password: {password}
...""".format(username=PLUGIN_NAME, password=GENERIC_PASSWORD).encode("utf-8")


def test_secure_store_fixture(testdir, tmpdir):
    """Make sure that pytest accepts the store fixture."""
    # create a temporary, encrypted data file from YML_FILE
    file = tmpdir.join('encrypt.test')
    with open(file, "wb") as encrypt_test:
        stream = BytesIO(YML_FILE)
        encryptStream(stream, encrypt_test, GENERIC_PASSWORD, BUFFER_SIZE)

    # create a temporary pytest test module
    testdir.makepyfile(
        "\n" +
        "    def test_seek(store):\n" +
        "        assert store == {}\n".format(load_yaml(YML_FILE))
    )

    # run pytest with the following CL args
    result = testdir.runpytest(
        '--secure-store-password={}'.format(GENERIC_PASSWORD),
        "--secure-store-filename={}".format(file),
        "-s",
        "-v"
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        "test_secure_store_fixture.py::test_seek PASSED"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(testdir):
    """Test the securestore plugin help is displayed in Py.Test's help."""
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        "Secure storage:",
        "*--secure-store-password=SECURE_STORE_PASSWORD",
        "*Set the secure storage decryption password.*",
        "*--secure-store-filename=SECURE_STORE_FILENAME",
        "*Set the secure storage path and filename.",
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_secure_storage_setting(testdir):
    """Test the INI configuration loads."""
    testdir.makeini("""
        [pytest]
        secure_store_filename = {file}
        secure_store_password = {password}
    """.format(file=PLUGIN_NAME, password=GENERIC_PASSWORD))

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def store(request):
            return [request.config.getini('secure_store_filename'),
                    request.config.getini('secure_store_password')]

        def test_secure_storage_ini_settings(store):
            assert store == ['{file}', '{password}']
    """.format(file=PLUGIN_NAME, password=GENERIC_PASSWORD))

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_secure_storage_ini_settings PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

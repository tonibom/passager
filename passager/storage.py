#!/bin/python3
"""
Storage module is responsible for handling the data storage. Salting and hashing
is applied to the main account's information in order to ensure password
security. However, as this is a password manager, the service account passwords
need to be retrievable so hashing won't do. Encryption using the main account's
password as a base for the key is therefore used instead.
"""
import os
import logging

from typing import Optional, Sequence

from passager.data_formats import MainAccount, ServiceAccount

# TODO: Platform independency
_FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + "/accounts/"
_FILE_EXT = ".txt"
# TODO: Adjust
_KEY_LENGTH = 128

_logger = logging.getLogger(__name__)


def _compare_hash(first_hash: str, second_hash: str) -> bool:
    differences = 0
    if len(first_hash) != len(second_hash):
        _logger.debug("Length mismatch: %s =/= %s", len(first_hash), len(second_hash))
        differences += 1
    for i in range(len(first_hash)):
        try:
            if first_hash[i] != second_hash[i]:
                _logger.debug("Hash char mismatch: %s =/= %s", first_hash[i], second_hash[i])
                differences += 1
        except IndexError:
            # The hashes weren't equally long
            differences += 1
            pass
    # TODO: remove
    _logger.debug("Differences %s", differences)
    return differences == 0


def _decrypt(string: str, key: str) -> str:
    return string


def delete_main_account(main_account: MainAccount):
    # TODO: Derive decryption key from username
    username_file = main_account.account_name + _FILE_EXT
    file_path = _FILE_DIR + username_file

    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        _logger.warning("ERROR: Couldn't remove main account file as it doesn't exist!")


def delete_service_account(main_pass: str,
                           service_name: str):
    # TODO: Derive encryption key from main password

    # TODO: Encrypt service name using the key
    filename = service_name

    file_path = _FILE_DIR + filename + _FILE_EXT

    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        _logger.warning("ERROR: Couldn't remove service account file as it doesn't exist!")


def _encrypt(string: str, key: str) -> str:
    return string


def _generate_salt() -> str:
    # TODO: generate unique salt
    # Hint: Use os.urandom
    return ""


def get_usernames() -> Optional[Sequence[str]]:
    filenames = _read_filenames()
    # TODO: Fix Bug - if filename ends with t, removes that as well...
    # Should only remove the .txt, not t.txt
    filenames = [filename.rstrip(_FILE_EXT) for filename in filenames]
    return filenames


def load_service_accounts(main_account: MainAccount):
    filenames = _read_filenames()
    for filename in filenames:
        # TODO: Derive decryption key from main_pass
        # TODO: Decrypt filenames using decryption key
        # TODO: Fix Bug - if filename ends with t, removes that as well...
        # Should only remove the .txt, not t.txt
        service_name = filename.rstrip(_FILE_EXT)
        if len(service_name) == _KEY_LENGTH:
            # This file didn't contain a service account for this main account
            continue
        # Decrypted successfully -> it's a correct service
        contents = _read_file(filename)
        if len(contents) == 1:
            _logger.debug("Tried to access main account as service account...")
            continue
        if len(contents) != 2:
            _logger.warning("Unknown account file encountered when loading service accounts!")
            continue

        # TODO: Decrypt contents
        try:
            username = contents[0]
            password = contents[1]
        except IndexError:
            # Problem with valid file detection
            _logger.warning("Index error in service account load!")
            continue
        service = ServiceAccount(service_name,
                                 username,
                                 password)
        main_account.service_accounts.append(service)


def _read_file(filename: str) -> Sequence[str]:
    # TODO: Encrypt filename
    # TODO: Platform indepedency
    file_path = _FILE_DIR + filename
    with open(file_path, "r") as source:
        # Remove the newlines
        # TODO: Could it be that this interferes with encryption / hashing?
        contents = [a.rstrip("\n") for a in source.readlines()]
    return contents


def _read_filenames() -> Sequence[str]:

    files_list = [f for f in os.listdir(_FILE_DIR) if os.path.isfile(os.path.join(_FILE_DIR, f))]
    _logger.debug("Retrieved files list: %s", files_list)
    return files_list


def salt_and_hash(password: str, salt: str) -> str:
    # TODO: hash
    hashed_pass = password
    return salt + hashed_pass


def store_main_account(main_account: MainAccount):

    if main_account.salt is None:
        main_account.salt = _generate_salt()
    filename = main_account.account_name
    # TODO: Salt & hash the password
    salted_hash = salt_and_hash(main_account.main_pass, main_account.salt)

    _write_file(filename, salted_hash)


def store_service_account(main_pass: str, service_account: ServiceAccount):
    # TODO: Derive encryption key from main password

    # TODO: Encrypt service name
    filename = service_account.service_name
    # TODO: Encrypt password
    service_password = service_account.service_password
    # TODO: Encrypt username
    service_username = service_account.account_name

    _write_file(filename, service_password, service_username)


def validate_main_login(username: str, password: str) -> Optional[MainAccount]:
    main_account = None

    # TODO: Derive decryption key from username
    username_file = username + _FILE_EXT
    filenames = _read_filenames()
    # TODO: Derive decryption key from password
    # TODO: Decrypt filenames with decryption key

    # TODO: Consider timing attacks
    if username_file in filenames:
        # Account exists
        contents = _read_file(username_file)
        if len(contents) != 1:
            return None
        actual_password = contents[0]
        if _compare_hash(password, actual_password):
            # Login successful
            # TODO: Fix
            salt = "AAAA"
            main_account = MainAccount(username, password, salt)

    return main_account


def _write_file(filename: str, password: str, accountname: str = None):
    # For main accounts filename is the account's name as plain text and
    # accountname is None.
    # For service accounts filename is the service's name as encrypted and
    # accountname is the account's username also as encrypted (with a key
    # derived from the main account's password).

    file_path = _FILE_DIR + filename + _FILE_EXT
    with open(file_path, "w") as source:
        source.write(password + "\n")
        if accountname is not None:
            # Only service accounts have this one stored
            source.write(accountname + "\n")

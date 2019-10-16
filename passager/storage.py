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


def _encrypt(string: str, key: str) -> str:
    return string


def _generate_salt() -> str:
    # TODO: generate unique salt
    # Hint: Use os.urandom
    return ""


def load_password_hash(user: str, service: str) -> str:
    return ""


def load_service_accounts(main_account: MainAccount):
    filenames = _read_filenames()
    for filename in filenames:
        # TODO: Derive decryption key from main_pass
        # TODO: Decrypt filenames using decryption key
        service_name = filename.rstrip(_FILE_EXT)
        if len(service_name) == _KEY_LENGTH:
            # This file didn't contain a service account for this main account
            continue
        # Decrypted successfully -> it's a correct service
        contents = _read_file(filename)
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


def salt_and_hash_new(password: str) -> str:
    # New as in password hasn't been salted and hashed before
    salt = _generate_salt()
    # TODO: hash
    hashed_pass = password
    return salt + hashed_pass


def salt_and_hash(password: str, salt: str) -> str:
    # TODO: hash
    hashed_pass = password
    return salt + hashed_pass


def store_password_hash(password: str, user: str, service: str):
    pass


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
        actual_password = contents[0]
        if _compare_hash(password, actual_password):
            # Login successful
            account_name = contents[1]
            # TODO: Fix
            salt = "AAAA"
            main_account = MainAccount(username, password, salt)

    return main_account


def _write_file(filename, password, accountname):
    # TODO: Encrypt filename

    file_path = _FILE_DIR + filename + _FILE_EXT
    with open(file_path, "w") as source:
        source.write(password + "\n")
        source.write(accountname + "\n")

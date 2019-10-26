#!/bin/python3
"""
The module that contains the data formats used internally within the software.
"""
import base64
import enum
import re
from typing import Optional, Sequence

IV_LENGTH = 16
# TODO: Adjust
KEY_LENGTH = 256
PASSWORD_MAX_LENGTH = 128
PASSWORD_MIN_LENGTH = 12
# TODO: Adjust
SALT_LENGTH = 16  # 128 bits
USERNAME_MAX_LENGTH = 32
USERNAME_MIN_LENGTH = 6


class MenuOptions(enum.IntEnum):
    HELP = 0
    TRAINING = 1
    SERVICE_ACCOUNT_ADD = 2
    SERVICE_ACCOUNT_CHANGE_PASSWORD = 3
    SERVICE_ACCOUNT_REMOVE = 4
    SERVICE_ACCOUNTS = 5
    MAIN_ACCOUNT_CHANGE_PASSWORD = 6
    MAIN_ACCOUNT_REMOVE = 7
    LOGOUT = 8


class MainAccount:
    def __init__(self, account_name: str, main_pass: str, salt: bytes = None):
        self.service_accounts = []
        self.account_name = account_name
        self.main_pass = main_pass
        self.salt = salt

    def change_password(self, new_password: str):
        self.main_pass = new_password
        # Reset salt so that it shall be generated again
        self.salt = None

    def remove_service_account(self, service_name: str):
        if service_name not in self.service_names():
            return
        account = self.service_account_by_name(service_name)
        if account is not None:
            self.service_accounts.remove(account)
            return

    def service_account_by_name(self, service_name: str) -> Optional["ServiceAccount"]:
        for account in self.service_accounts:
            if account.service_name == service_name:
                return account

    def service_names(self) -> Sequence[str]:
        names = []
        for account in self.service_accounts:
            names.append(account.service_name)
        return names


class ServiceAccount:
    def __init__(self, service_name: str, account_name: str, service_password: str):
        self.service_name = service_name
        self.account_name = account_name
        self.service_password = service_password

    def change_password(self, new_password):
        self.service_password = new_password


def check_password_strength(password: str) -> int:
    # 0: Poor
    # 1: Weak
    # 2: Adequate
    # 3: Mediocre
    # 4: Strong
    # 5: Very strong
    # TODO: Could improve upon this classification to be more helpful
    # TODO: as currently it only considers bruteforcing but not dictionaries
    # TODO: Adjust.
    if len(password) >= 20:
        return 5
    elif len(password) >= 15:
        return 4
    elif len(password) > 12:
        return 3
    # Number of
    digits = len(re.findall("[0-9]", password))
    lower_case = len(re.findall("[a-z]", password))
    upper_case = len(re.findall("[A-Z]", password))
    if digits == 0 or lower_case == 0 or upper_case == 0:
        return 1
    elif digits >= 3 and lower_case >= 3 and upper_case >= 3:
        return 3
    return 2


# TODO: Fix the naming and the usages of the following functions
#  The following encoding & decoding functions are used in different places
#  and for different things. Naming is really bad in this section as these
#  saw a lot of revisions before they finally worked as intended.


def decode_load(input_bytes: bytes) -> str:
    # Used in
    #     decrypt_contents for CONTENTS
    #     decrypt_filename for SERVICE_NAME
    # AKA LOAD DECRYPTION
    return input_bytes.decode("utf-8")


def decode_store(input_bytes: bytes) -> str:
    # Used in
    #     encrypt_filename for ENCRYPTED_FILENAME
    # AKA STORE ENCRYPTION
    return base64.b32encode(input_bytes).decode("utf-8")


def encode_general(string: str) -> bytes:
    # Used in
    #    derive_encryption_key for MAIN_PASS
    #    load_service_account for INIT_VECTOR
    #    salt_and_hash for PASSWORD
    # AKA almost everywhere
    return string.encode("utf-8")


def encode_load(string: str) -> bytes:
    # Used in
    #    load_service_account for INIT_VECTOR
    #    load_service_account for ENCRYPTED_SERVICE_NAME
    # AKA LOAD
    return base64.b32decode(string.encode("utf-8"))

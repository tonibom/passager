#!/bin/python3
"""
The module that contains the data formats used internally within the software.
"""
import enum
import re
from typing import Optional, Sequence

PASSWORD_MAX_LENGTH = 128
PASSWORD_MIN_LENGTH = 12
SALT_LENGTH = 32


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
    def __init__(self, account_name: str, main_pass: str, salt: str = None):
        self.service_accounts = []
        self.account_name = account_name
        self.main_pass = main_pass
        self.salt = salt

    def change_password(self, new_password):
        self.main_pass = new_password

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

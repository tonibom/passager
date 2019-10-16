#!/bin/python3
"""
The module that contains the data formats used internally within the software.
"""
import enum
from typing import Optional, Sequence

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
    def __init__(self, account_name: str, main_pass: str, salt: str):
        self.service_accounts = []
        self.account_name = account_name
        self.main_pass = main_pass
        self.salt = salt

    @staticmethod
    def register_account(name: str, password_hash: str, salt: str)\
            -> Optional["MainAccount"]:
        """Returns account if it can be registered.
        Otherwise returns None
        """
        # TODO: Check that the account name is available
        return MainAccount(name, password_hash, salt)

    def remove_service_account(self, service_name: str):
        if service_name not in self.service_names():
            return
        for account in self.service_accounts:
            if account.service_name == service_name:
                self.service_accounts.remove(account)
                return

    def service_names(self) -> Sequence[str]:
        names = []
        for account in self.service_accounts:
            names.append(account.service_name)
        return names

    @staticmethod
    def validate_password(password: str) -> bool:
        # TODO: Strength check
        pass


class ServiceAccount:
    def __init__(self, service_name: str, account_name: str, service_password: str):
        self.service_name = service_name
        self.account_name = account_name
        self.service_password = service_password


def slow_hash_compare():
    # TODO: Slow string comparison to avoid timing attacks
    pass
